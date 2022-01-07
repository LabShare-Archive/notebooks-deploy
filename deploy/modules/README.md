Instructions to manually recreate external environment modules used by JupyterLab

1. Create a special JupyterLab pod with a write access to modules volume
```
```
2. Get a shell to the pod
2a. Using command line of choice, by running
```
kubectl exec -it ...
```
2b. Using VSCode with installed Kubernetes extension
- Open Kubernetes panel on the left
- Click on the relevant Kubernetes context
- Click on Workloads -> Pods
- Find `env-installer-xxx` and right-click it
- Click on Attach Visual Studio Code

New window will open with access to the file system and Terminal. Open folder `/opt/modules`

3. Run the scripts to create the modules

Common setup for all modules:
```
export EXT_MOD_PATH=/opt/modules
```

a. Python Data Science
- Make sure to copy the `python-data-science-env-<x.y.z>.yaml` file to the pod first
- Install the Conda environment
```
export PYTHON_DS_ENV_VERSION=<x.y.z>
mkdir -p $EXT_MOD_PATH/conda-envs/python-data-science-$PYTHON_DS_ENV_VERSION
mamba env create --prefix $EXT_MOD_PATH/conda-envs/python-data-science-$PYTHON_DS_ENV_VERSION --file python-data-science-env-$PYTHON_DS_ENV_VERSION.yaml
```
- Create environment module folder
```
mkdir -p $EXT_MOD_PATH/modulefiles/python-data-science
```
- Create the environment module file at `` with the following content:
```
help([[
Conda environment with Python Data Science packages
]])

whatis("Version: 0.1.0")
whatis("Keywords: Data Science")

prepend_path("JUPYTER_PATH", "/opt/modules/conda-envs/python-data-science-<x.y.z>/share/jupyter")
```

Make sure to replace <x.y.z> with the module version
This module file makes Jupyter kernel from our custom environment visible to Jupyter executable. Kernel will show up instantly in the launcher when module is loaded.


b. R
```
export R_ENV_VERSION=<x.y.z>
mkdir -p $EXT_MOD_PATH/conda-envs/R-$R_ENV_VERSION

```
c. C++
d. Julia
e. Octave
```
export OCTAVE_ENV_VERSION=<x.y.z>
mkdir -p $EXT_MOD_PATH/conda-envs/octave-$OCTAVE_ENV_VERSION
mamba env create --prefix $EXT_MOD_PATH/conda-envs/octave-$OCTAVE_ENV_VERSION --file octave-env-$OCTAVE_ENV_VERSION.yaml
```