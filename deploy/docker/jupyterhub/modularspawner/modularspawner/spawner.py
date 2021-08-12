import os, subprocess
import requests
from kubespawner import KubeSpawner
from traitlets import (
    List,
    Unicode,
)

class ModularSpawner(KubeSpawner):
    def _options_form_default(self):
        """
        Generates html form to choose stacks from
        """
        
        # Prepend path to stacks folder
        self.base = os.path.join(self.stacks_path, self.base)
        self.stacks = [[os.path.join(self.stacks_path, s) for s in stack] for stack in self.stacks]

        self.options = [f'option{i+1}' for i in range(len(self.stacks))]
        
        self.form = """
<div class="form-group">
    Choose additional language kernels and/or packages. Loads with Python kernel by default:
    <br>"""
        
        for i in range(len(self.stacks)):
            self.form +=(f"""
    <input type="checkbox" id="option{i+1}" name="option{i+1}">
    <label for="option1">{self.stacks_names[i]}</label><br>""")
        
        self.form += """
</div>"""

        # Generate html form
        return self.form

    def options_from_form(self, formdata):
        # Decode user choices        
        options = [True if formdata.get(option, None) else False for option in self.options]
        
        # Get image hash by running `polus-railyard`
        tag = subprocess.run(('railyard hash ' + '-b ' + self.base + ''.join([f' -a {item}' for stack,included in zip(self.stacks,options) for item in stack if included])).split(' '), capture_output=True).stdout.decode("utf-8").rstrip()
        self.log.debug("Spawning tag: %s", tag)

        #Check if image exist to avoid PullErrors
        if requests.get('https://hub.docker.com/v2/repositories/labshare/polyglot-notebook/tags/' + tag).status_code != 200:
            #if image does not exist, switch to the maximal image with all stacks included
            self.log.debug("Requested tag %s is not in registry, using default image", tag)
            options = [True] * len(self.stacks)
            tag = subprocess.run(('railyard hash ' + '-b ' + self.base + ''.join([f' -a {item}' for stack,included in zip(self.stacks,options) for item in stack if included])).split(' '), capture_output=True).stdout.decode("utf-8").rstrip()
        
        # Get full image tag
        image = 'labshare/polyglot-notebook:' + tag

        # Update profile list
        profile={'display_name': tag, 'default': True, 'kubespawner_override': {'image': image}}

        profile_list = self.profile_list
        profile_list.append(profile)
        setattr(self, 'profile_list', profile_list)
        
        return dict(profile_list=profile_list)
    
    async def load_user_options(self):
        """Load user options from self.user_options dict
        This can be set via POST to the API or via options_from_form
        Overrides the KubeSpawner's load_user_options to support 'request_profile'
        """
        
        if self._profile_list is None:
            if callable(self.profile_list):
                profile_list = await gen.maybe_future(self.profile_list(self))
            else:
                profile_list = self.profile_list

            self._profile_list = self._init_profile_list(profile_list)

        # TODO: Check if new profile was requested
        # 

        selected_profile = self.user_options.get('profile', None)
        if self._profile_list:
            await self._load_profile(selected_profile)
        elif selected_profile:
            self.log.warning(
                "Profile %r requested, but profiles are not enabled", selected_profile
            )

        # help debugging by logging any option fields that are not recognized
        option_keys = set(self.user_options)
        unrecognized_keys = option_keys.difference(self._user_option_keys)
        if unrecognized_keys:
            self.log.warning(
                "Ignoring unrecognized KubeSpawner user_options: %s",
                ", ".join(map(str, sorted(unrecognized_keys))),
            )
    
    stacks_path = Unicode(
        config=True,
        help="""
        Location of all stacks
        """
    )

    base = Unicode(
        config=True,
        help="""
        Base stack filename
        """
    )

    stacks = List(
        config=True,
        help="""
        List of lists of stacks filenames in the format:
            stacks = [['stack1.yaml', 'stack2.yaml'], ['stack3.yaml'], ['stack4.yaml']]
        """
    )
    
    stacks_names = List(
        config=True,
        help="""
        List of stacks' names in the format:
            stacks_names = ['Name A', 'Name B', 'Name C']
        Lengths of ModularSpawner.stacks and ModularSpawner.stacks_names must be the same
        """
    )
