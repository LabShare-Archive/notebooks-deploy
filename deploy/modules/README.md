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
f. Java 8
```
mkdir -p $EXT_MOD_PATH/java-8
wget https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u312-b07/OpenJDK8U-jdk_x64_linux_hotspot_8u312b07.tar.gz
tar xvf OpenJDK8U-jdk_x64_linux_hotspot_8u312b07.tar.gz -C $EXT_MOD_PATH/java-8/
```
g. Java 11
```
mkdir -p $EXT_MOD_PATH/java-11
wget https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.13%2B8/OpenJDK11U-jdk_x64_linux_hotspot_11.0.13_8.tar.gz
tar xvf OpenJDK11U-jdk_x64_linux_hotspot_11.0.13_8.tar.gz -C $EXT_MOD_PATH/java-11/
```
h. Java 17
```
mkdir -p $EXT_MOD_PATH/java-17
wget https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.1%2B12/OpenJDK17U-jdk_x64_linux_hotspot_17.0.1_12.tar.gz
tar xvf OpenJDK17U-jdk_x64_linux_hotspot_17.0.1_12.tar.gz -C $EXT_MOD_PATH/java-17/
```
i. IJava kernel
Install into each of the supported JDK installations (JDK>=9)
```
curl -L https://github.com/SpencerPark/IJava/releases/download/v1.3.0/ijava-1.3.0.zip > ijava-kernel.zip
unzip ijava-kernel.zip -d ijava-kernel 
cd ijava-kernel
python install.py --prefix=/opt/modules/java-11/
curl -L https://www.pngall.com/wp-content/uploads/2016/05/Java-PNG-Image.png > /opt/modules/java-11/share/jupyter/kernels/java/logo-64x64.png
```
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

Modify kernel.js to swap `` with `/opt/modules/conda-envs/js-0.1.0/bin/ijskernel`