import os, sys
import string
import pickle
import escapism
from oauthenticator.generic import GenericOAuthenticator
from jupyterhub.auth import DummyAuthenticator

# Make sure that modules placed in the same directory as the jupyterhub config are added to the pythonpath
configuration_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, configuration_directory)

from z2jh import get_config, get_secret_value

release_name = get_config("Release.Name")
chart_name = get_config("Chart.Name")
wipp_enabled = get_config("hub.wipp.enabled")
polus_notebooks_hub_enabled = get_config("hub.polusNotebooksHub.enabled")
monitoring_enabled = get_config("hub.monitoring.enabled")

c.JupyterHub.spawner_class = "kubespawner.KubeSpawner"
c.KubeSpawner.start_timeout = 1000

c.KubeSpawner.default_url = "/lab"
c.KubeSpawner.uid = 1000  # uid 1000 corresponds to jovyan, uid 0 to root
c.KubeSpawner.cmd = ["jupyter-labhub"]
c.KubeSpawner.args = ["--collaborative"]
c.KubeSpawner.working_dir = "/home/jovyan"
c.KubeSpawner.service_account = f"{release_name}-{chart_name}-user"
c.KubeSpawner.singleuser_image_pull_policy = "Always"
c.KubeSpawner.pod_name_template = (
    f"{release_name}-{chart_name}-lab-{{username}}--{{servername}}"
)

# Volumes to attach to Pod
c.KubeSpawner.volumes = [
    {
        "name": "notebooks-volume",
        "persistentVolumeClaim": {
            "claimName": f'{release_name}-{chart_name}-hub-{get_config("hub.storage.notebooksClaimName")}'
        },
    },
    {
        "name": "modules-volume",
        "persistentVolumeClaim": {
            "claimName": f'{release_name}-{chart_name}-hub-{get_config("hub.storage.modulesClaimName")}'
        },
    },
]
if wipp_enabled:
    c.KubeSpawner.volumes.append(
        {
            "name": "wipp-volume",
            "persistentVolumeClaim": {
                "claimName": get_config("hub.wipp.storageClaimName")
            },
        }
    )

# Where to mount volumes
c.KubeSpawner.volume_mounts = [
    {
        "mountPath": "/home/jovyan/work",
        "name": "notebooks-volume",
        "subPath": f"{{username}}",
    },
    {
        "mountPath": "/opt/shared/notebooks",
        "name": "notebooks-volume",
        "subPath": "shared",
    },
    {"mountPath": "/opt/modules", "name": "modules-volume", "readOnly": True},
]
if wipp_enabled:
    c.KubeSpawner.volume_mounts.append(
        {"mountPath": get_config("hub.wipp.mountPath"), "name": "wipp-volume"}
    )

c.KubeSpawner.image = "labshare/polyglot-notebook:" + get_config("hub.notebookVersion")

# Create Hub profiles
jupyterlab_profile = {
    "display_name": f"JupyterLab",
    "slug": f"jupyterlab",
    "profile_options": {},
    "default": True,
}

# Create profiles based on hardware options
hardware_options = {}
if get_config("hub.hardwareOptions"):
    for hardwareOptionName, hardwareOption in get_config("hub.hardwareOptions").items():
        hardware_options.update(
            {
                hardwareOptionName: {
                    "display_name": hardwareOption["name"],
                    "slug": f'jupyterlab{hardwareOption["slugSuffix"]}',
                    "kubespawner_override": {
                        "image": f'labshare/polyglot-notebook:{get_config("hub.notebookVersion")}{hardwareOption["imageTagSuffix"]}',
                        **(lambda name, slugSuffix, imageTagSuffix, **kw: kw)(
                            **hardwareOption
                        ),
                    },
                }
            }
        )

if hardware_options:
    # Single hardware option
    if len(hardware_options) == 1:
        single_hardware_option = next(iter(hardware_options.values()))
        jupyterlab_profile["slug"] = single_hardware_option["slug"]
        jupyterlab_profile["kubespawner_override"] = single_hardware_option[
            "kubespawner_override"
        ]
    # Multiple hardware options
    if len(hardware_options) > 1:
        jupyterlab_profile["profile_options"].update(
            {"hardwareOptions": {"display_name": "Memory", "choices": hardware_options}}
        )

c.KubeSpawner.profile_list = []
c.KubeSpawner.profile_list.append(jupyterlab_profile)

if polus_notebooks_hub_enabled:
    c.KubeSpawner.profile_list.extend(
        [
            {
                "display_name": "Streamlit Dashboard",
                "slug": "jhsingle-streamlit-variable",
                "kubespawner_override": {"image": "polusai/hub-streamlit"},
            },
            {
                "display_name": "Voila Dashboard",
                "slug": "jhsingle-voila-variable",
                "kubespawner_override": {"image": "polusai/hub-voila"},
            },
        ]
    )

c.JupyterHub.allow_named_servers = True
c.JupyterHub.ip = "0.0.0.0"
c.JupyterHub.hub_ip = "0.0.0.0"

# Required for AWS
c.JupyterHub.hub_connect_ip = f"{release_name}-{chart_name}-internal"

# configure the JupyterHub database
if get_config("postgresql.enabled"):
    postgres_db = get_config("postgresql.auth.database")
    postgres_user = get_config("postgresql.auth.username")
    postgres_password = get_config("postgresql.auth.password")
    c.JupyterHub.db_url = (
        "postgresql://"
        + postgres_user
        + ":"
        + postgres_password
        + "@"
        + release_name
        + "-postgresql-hl"
        + "/"
        + postgres_db
    )
else:
    c.JupyterHub.db_url = "sqlite:///jupyterhub.sqlite"

c.JupyterHub.cleanup_servers = False
c.JupyterHub.cookie_secret_file = "/srv/jupyterhub/jupyterhub_cookie_secret"

if get_config("hub.auth.enabled"):
    # Default authenticator in production is OAuth with LabShare
    c.JupyterHub.authenticator_class = GenericOAuthenticator
    OAUTH_CLIENT_ID = os.getenv("OAUTH_CLIENT_ID")
    OAUTH_CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET")
    ADMIN_USERS = os.getenv("ADMIN_USERS")
    ADMIN_SERVICE_ACC = os.getenv("ADMIN_SERVICE_ACC")

    c.Authenticator.admin_users = set(ADMIN_USERS.split(";"))

    c.GenericOAuthenticator.client_id = OAUTH_CLIENT_ID
    c.GenericOAuthenticator.client_secret = OAUTH_CLIENT_SECRET
    c.GenericOAuthenticator.username_key = "email"
    c.GenericOAuthenticator.userdata_method = "GET"
    c.GenericOAuthenticator.extra_params = dict(
        client_id=OAUTH_CLIENT_ID, client_secret=OAUTH_CLIENT_SECRET
    )
    c.GenericOAuthenticator.basic_auth = False
    c.GenericOAuthenticator.auto_login = True
else:
    # Fallback to DummyAuthenticator if no auth is configured
    c.JupyterHub.authenticator_class = DummyAuthenticator

# Configure JupyterHub services
services = [
    {
        # Service to shutdown inactive Notebook servers after --timeout seconds
        "name": "cull-idle",
        "command": [
            sys.executable,
            "-m",
            "jupyterhub_idle_culler",
            f"--timeout={3600 * int(get_config('hub.culling.timeout'))}",
            "--remove-named-servers",
        ],
    },
    {
        # Admin service (used in Notebooks Hub and config-wrapper)
        "name": "service-token",
        "api_token": get_secret_value("adminToken"),
    },
]

if monitoring_enabled:
    services.append(
        {
            # Monitoring service (used in Notebooks Hub and config-wrapper)
            "name": "monitoring",
            "api_token": get_secret_value("monitoringToken"),
        }
    )

c.JupyterHub.services = services

# Read the users and groups backed up by config-wrapper
try:
    infile = open("users.pkl", "rb")
    users = pickle.load(infile)
    infile.close()
except:
    users = []

try:
    infile = open("groups.pkl", "rb")
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

    group = {
        f"server_sharing_{safe_username}": groups_backup.get(
            f"server_sharing_{safe_username}", []
        )
    }
    groups.update(group)

    sharing_role = {
        "name": f"server_sharing_{safe_username}_role",
        "description": f"Server sharing of {user}",
        "scopes": [f"access:servers!user={user}"],
        "groups": [f"server_sharing_{safe_username}"],
    }

    sharing_group_editing_role = {
        "name": f"server_sharing_{safe_username}_group_editing_role",
        "description": f"Edit server_sharing_{safe_username} group",
        "scopes": [f"groups!group=server_sharing_{safe_username}"],
        "users": [user],
    }

    usernames_reading_role = {
        "name": f"usernames_reading_{safe_username}_role",
        "description": "Usernames reading group",
        "scopes": ["list:users"],
        "users": [user],
    }

    roles.append(sharing_role)
    roles.append(sharing_group_editing_role)
    roles.append(usernames_reading_role)

# Required for getting user reading scope in the JUPYTERHUB_API_TOKEN on user server
roles.append(
    {
        "name": "server",
        "scopes": ["inherit"],
    }
)

roles.append(
    {
        "name": "admin-role",
        "scopes": ["admin:users", "admin:groups", "admin:servers"],
        "services": ["service-token"],
    }
)

if monitoring_enabled:
    roles.append(
        {
            "name": "monitoring-role",
            "scopes": ["read:metrics"],
            "services": ["monitoring"],
        }
    )

roles.append(
    {
        "name": "cull-idle-role",
        "scopes": [
            "list:users",
            "read:users:activity",
            "read:servers",
            "delete:servers",
        ],
        "services": [
            "cull-idle",
        ],
    }
)

c.JupyterHub.load_groups = groups
c.JupyterHub.load_roles = roles

# Set up environment variables
c.KubeSpawner.environment = {
    "CONDA_ENVS_PATH": "/opt/modules/conda-envs/",
    "LMOD_SYSTEM_DEFAULT_MODULES": lambda spawner: str(
        spawner.user_options.get("modules", "StdEnv")
    ),  # Get the list of modules from user options or fall back to the StdEnv
    "MODULEPATH": "/opt/modules/modulefiles",
    "USER_OPTIONS": lambda spawner: str(spawner.user_options),
}

# Set up WIPP-related environment variables
if wipp_enabled:
    c.KubeSpawner.environment.update(
        {
            "WIPP_UI_URL": get_config("hub.wipp.UIValue"),
            "WIPP_API_INTERNAL_URL": get_config("hub.wipp.apiURL"),
            "WIPP_NOTEBOOKS_PATH": os.path.join(
                get_config("hub.wipp.mountPath"),
                get_config("hub.wipp.tempNotebooksRelPath"),
            ),
            "PLUGIN_TEMP_PATH": os.path.join(
                get_config("hub.wipp.mountPath"),
                get_config("hub.wipp.tempPluginsRelPath"),
            ),
        }
    )

# Set up Polus Notebooks Hub environment variables
if polus_notebooks_hub_enabled:
    c.KubeSpawner.environment.update(
        {
            "POLUS_NOTEBOOKS_HUB_API": get_config("hub.polusNotebooksHub.apiURL"),
            "POLUS_NOTEBOOKS_HUB_FILE_LOGGING_ENABLED": "True",
        }
    )
