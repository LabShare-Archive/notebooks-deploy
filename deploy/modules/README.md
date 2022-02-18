# Installation instructions

Following the deployment of the Helm Chart, you will need to install the environment modules to enable different kernels for users. This repository provides the modules created for testing and internal use, but it is possible to modify those or create your own.

The installation of environment modules is performed using K8s Jobs and configMaps. ConfigMap allows to provide the context for the installer, i.e. conda environment definitions and modulefiles, whereas the Job lists the environment variables specifiying the metadata, i.e. the version of the environment module to be installed, as well as the shell commands requied to install the environment module to the shared modules volume.

When using the existing installer, the installation process is a single line CLI command:

```
kubectl apply -f <environment-module-name>-<x.y.z>.yaml
```

This would start the installation process, which can take between minutes to an hour. You can monitor the status of the installation using:

```
kubectl describe job <environment-module-name>-<x-y-z>-installer-job
```

and check the installation logs with

```
kubectl logs job/<environment-module-name>-<x-y-z>-installer-job
```

| Kernel              | Version   | Installer            |
| ------------------- | --------- | -------------------- |
| Python Data Science | 0.1.0     |                      |
| R                   | 0.1.0     | r-0.1.0-job.yaml     |
| Chemoinformatics    | 0.1.0     | rdkit-0.1.0-job.yaml |
| C++                 | 0.1.0     |                      |
| Julia               |           |                      |
| Octave              |           |                      |
| Java                | 1.8.0_312 |                      |
| Java                | 11.0.3    |                      |
| Java                | 17.0.1    |                      |
| Maven               |           |                      |
| JavaScript          |           |                      |

a. Python Data Science

- Create environment module folder

```

mkdir -p $EXT_MOD_PATH/modulefiles/python-data-science

```

- Create the environment module file at `` with the following content:

```

help([[Conda environment with Python Data Science packages]])

whatis("Version: 0.1.0")
whatis("Keywords: Data Science")

prepend_path("JUPYTER_PATH", "/opt/modules/conda-envs/python-data-science-<x.y.z>/share/jupyter")

```

Make sure to replace <x.y.z> with the module version
This module file makes Jupyter kernel from our custom environment visible to Jupyter executable. Kernel will show up instantly in the launcher when module is loaded.

k. Maven

```

mkdir -p $EXT_MOD_PATH/maven-3.6.3
wget https://archive.apache.org/dist/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz
tar xvf apache-maven-3.6.3-bin.tar.gz -C $EXT_MOD_PATH/opt/modules/maven-3.6.3

```

l. Javascript
Docs: http://n-riesco.github.io/ijavascript/

```

export JS_ENV_VERSION=<x.y.z>
mkdir -p $EXT_MOD_PATH/conda-envs/js-$JS_ENV_VERSION
mamba env create --prefix $EXT_MOD_PATH/conda-envs/js-$JS_ENV_VERSION --file js-env-$JS_ENV_VERSION.yaml
/opt/modules/conda-envs/js-$JS_ENV_VERSION/bin/npm install -g ijavascript
/opt/modules/conda-envs/js-$JS_ENV_VERSION/bin/ijsinstall --spec-path=full
mkdir -p /opt/modules/conda-envs/js-$JS_ENV_VERSION/share/jupyter/kernels/javascript
mv /home/jovyan/.local/share/jupyter/kernels/javascript /opt/modules/conda-envs/js-$JS_ENV_VERSION/share/jupyter/kernels/javascript

```

Modify kernel.js to swap ``with`/opt/modules/conda-envs/js-0.1.0/bin/ijskernel`

```

```
