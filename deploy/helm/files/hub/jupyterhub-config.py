import os,sys
import string
import pickle
import escapism
from oauthenticator.generic import GenericOAuthenticator
from jupyterhub.auth import DummyAuthenticator

# Make sure that modules placed in the same directory as the jupyterhub config are added to the pythonpath
configuration_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, configuration_directory)

from z2jh import (
    get_config,
    get_secret_value
)

release_name = get_config("Release.Name")
chart_name = get_config("Chart.Name")
wipp_enabled = get_config("hub.wipp.enabled")
polus_notebooks_hub_enabled = get_config("hub.polusNotebooks.enabled")

c.JupyterHub.spawner_class = 'kubespawner.KubeSpawner'
c.KubeSpawner.start_timeout=1000

c.KubeSpawner.default_url = '/lab'
c.KubeSpawner.uid = 1000 #uid 1000 corresponds to jovyan, uid 0 to root
c.KubeSpawner.cmd = ['jupyter-labhub']
c.KubeSpawner.args = ['--collaborative']
c.KubeSpawner.working_dir = '/home/jovyan'
c.KubeSpawner.service_account='jupyteruser-sa'
c.KubeSpawner.singleuser_image_pull_policy= 'Always'
c.KubeSpawner.pod_name_template = f'{release_name}-{chart_name}-lab-{{username}}--{{servername}}'

# Per-user storage configuration
c.KubeSpawner.pvc_name_template = 'claim-{username}'
c.KubeSpawner.storage_class = get_config("global.storageClass")
c.KubeSpawner.storage_capacity = get_config("hub.storage.storagePerUser")
c.KubeSpawner.storage_access_modes = ['ReadWriteOnce']
c.KubeSpawner.storage_pvc_ensure = True

# Volumes to attach to Pod
c.KubeSpawner.volumes = [
    {
        'name': 'volume-{username}',
        'persistentVolumeClaim': {
            'claimName': 'claim-{username}'
        }
    },
    {
        'name': 'shared-volume',
        'persistentVolumeClaim': {
            'claimName': f'{release_name}-{chart_name}-hub-{get_config("hub.storage.sharedNotebooksClaimName")}'
        }
    },
    {
        'name': 'modules-volume',
        'persistentVolumeClaim': {
            'claimName': f'{release_name}-{chart_name}-hub-{get_config("hub.storage.modulesClaimName")}'
        }
    }
]
if wipp_enabled:
    c.KubeSpawner.volumes.append({
        'name': 'wipp-volume',
        'persistentVolumeClaim': {
            'claimName': get_config("hub.wipp.storageClaimName")
        }
    })

# Where to mount volumes
c.KubeSpawner.volume_mounts = [
    {
        'mountPath': '/home/jovyan/work',
        'name': 'volume-{username}'
    },
    {
        'mountPath': '/opt/shared/notebooks',
        'name': 'shared-volume'
    },
    {
        'mountPath': '/opt/modules',
        'name': 'modules-volume',
        'readOnly': True
    }
]
if wipp_enabled:
    c.KubeSpawner.volume_mounts.append(
        {
            'mountPath': get_config("hub.wipp.mountPath"),
            'name': 'wipp-volume'
        }
    )

c.KubeSpawner.image =  'labshare/polyglot-notebook:' + get_config("hub.notebookVersion")

if polus_notebooks_hub_enabled:
    c.KubeSpawner.profile_list = [
        {
            'display_name': 'JupyterLab',
            'slug': 'jupyterlab',
            'kubespawner_override': {
                'image': c.KubeSpawner.image
            }
        },
        {
            'display_name': 'Streamlit Dashboard',
            'slug': 'jhsingle-streamlit-variable',
            'kubespawner_override': {
                'image': 'polusai/hub-streamlit'
            }
        },
        {
            'display_name': 'Voila Dashboard',
            'slug': 'jhsingle-voila-variable',
            'kubespawner_override': {
                'image': 'polusai/hub-voila'
            }
        }
    ]

c.JupyterHub.allow_named_servers=True
c.JupyterHub.ip='0.0.0.0'
c.JupyterHub.hub_ip='0.0.0.0'

# Required for AWS
c.JupyterHub.hub_connect_ip='jupyterhub-internal'

# configure the JupyterHub database
if get_config("postgresql.enabled"):
    postgres_db = get_config("postgresql.auth.database")
    postgres_user = get_config("postgresql.auth.username")
    postgres_password = get_config("postgresql.auth.password")
    c.JupyterHub.db_url = 'postgresql://' + postgres_user + ':' + postgres_password + '@' + release_name + '-postgresql-hl' + '/' + postgres_db
else:
    c.JupyterHub.db_url = "sqlite:///jupyterhub.sqlite"

c.JupyterHub.cleanup_servers=False
c.JupyterHub.cookie_secret_file = '/srv/jupyterhub/jupyterhub_cookie_secret'

if get_config("hub.auth.enabled"):
    # Default authenticator in production is OAuth with LabShare
    c.JupyterHub.authenticator_class = GenericOAuthenticator
    OAUTH_CLIENT_ID = os.getenv('OAUTH_CLIENT_ID')
    OAUTH_CLIENT_SECRET = os.getenv('OAUTH_CLIENT_SECRET')
    ADMIN_USERS = os.getenv('ADMIN_USERS')
    ADMIN_SERVICE_ACC = os.getenv('ADMIN_SERVICE_ACC')

    c.Authenticator.admin_users = set(ADMIN_USERS.split(';'))

    c.GenericOAuthenticator.client_id = OAUTH_CLIENT_ID
    c.GenericOAuthenticator.client_secret = OAUTH_CLIENT_SECRET
    c.GenericOAuthenticator.username_key = "email"
    c.GenericOAuthenticator.userdata_method = "GET"
    c.GenericOAuthenticator.extra_params = dict(client_id=OAUTH_CLIENT_ID, client_secret=OAUTH_CLIENT_SECRET)
    c.GenericOAuthenticator.basic_auth = False
    c.GenericOAuthenticator.auto_login = True
else:
    # Fallback to DummyAuthenticator if no auth is configured
    c.JupyterHub.authenticator_class = DummyAuthenticator

# Read the users and groups backed up by config-wrapper
try:
    infile = open('users.pkl','rb')
    users = pickle.load(infile)
    infile.close()
except:
    users = []

try:
    infile = open('groups.pkl','rb')
    groups_backup = pickle.load(infile)
    infile.close()
except:
    groups_backup = {}

# Create RBAC groups and roles
groups = {}
roles = []

safe_chars = set(string.ascii_lowercase + string.digits)
for user in users:
    # Escape symbols not allowed in role and group names
    safe_username = escapism.escape(user, safe=safe_chars).lower()

    group = {f'server_sharing_{safe_username}': groups_backup.get(f'server_sharing_{safe_username}', [])}
    groups.update(group)

    sharing_role = {
        'name': f'server_sharing_{safe_username}_role',
        'description': f'Server sharing of {user}',
        'scopes': [f'access:servers!user={user}'],
        'groups': [f'server_sharing_{safe_username}']
    }

    sharing_group_editing_role = {
        'name': f'server_sharing_{safe_username}_group_editing_role',
        'description': f'Edit server_sharing_{safe_username} group',
        'scopes': [f'groups!group=server_sharing_{safe_username}'],
        'users': [user]
    }

    usernames_reading_role = {
        'name': f'usernames_reading_{safe_username}_role',
        'description': 'Usernames reading group',
        'scopes': ['list:users'],
        'users': [user]
    }

    roles.append(sharing_role)
    roles.append(sharing_group_editing_role)
    roles.append(usernames_reading_role)

# Required for getting user reading scope in the JUPYTERHUB_API_TOKEN on user server
roles.append({
    'name': 'server',
    'scopes': ['inherit'],
})

c.JupyterHub.load_groups = groups
c.JupyterHub.load_roles = roles

# Set up environment variables
c.KubeSpawner.environment = {
    'CONDA_ENVS_PATH': '/opt/modules/conda-envs/',
    'LMOD_SYSTEM_DEFAULT_MODULES': lambda spawner: str(spawner.user_options.get('modules', 'StdEnv')), #Get the list of modules from user options or fall back to the StdEnv
    'MODULEPATH': '/opt/modules/modulefiles',
    'USER_OPTIONS': lambda spawner: str(spawner.user_options),
}

# Set up WIPP-related environment variables
if get_config("hub.wipp.enabled"):
    c.KubeSpawner.environment.update({
        'WIPP_UI_URL': get_config("hub.wipp.UIValue"),
        'WIPP_API_INTERNAL_URL': get_config("hub.wipp.apiURL"),
        'WIPP_NOTEBOOKS_PATH': os.path.join(get_config("hub.wipp.mountPath"), get_config("hub.wipp.tempNotebooksRelPath")),
        'PLUGIN_TEMP_PATH': os.path.join(get_config("hub.wipp.mountPath"), get_config("hub.wipp.tempPluginsRelPath"))
    })

# Set up Polus Notebooks Hub environment variables
if get_config("hub.polusNotebooksHub.enabled"):
    c.KubeSpawner.environment.update({
        'POLUS_NOTEBOOKS_HUB_API': 'POLUS_NOTEBOOKS_HUB_API_VALUE',
        'POLUS_NOTEBOOKS_HUB_FILE_LOGGING_ENABLED': True
    })

c.JupyterHub.services = [
    {
        # Service to shutdown inactive Notebook servers after --timeout seconds
        'name': 'cull-idle',
        'admin': True,
        'command': [sys.executable, '/srv/jupyterhub/config/cull-idle-servers.py', '--timeout=3600'],
    },
    {
        # Service admin token (used in Notebooks Hub and config-wrapper)
        'name': 'service-token',
        'admin': True,
        'api_token': get_secret_value("adminToken"),
    }
]
