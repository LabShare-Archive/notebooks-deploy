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

| Kernel                  | Version   | Installer                          |
| ----------------------- | --------- | ---------------------------------- |
| Python Data Science     | 0.1.0     | python-data-science-0.1.1-job.yaml |
| R                       | 0.1.0     | r-0.1.0-job.yaml                   |
| Chemoinformatics        | 0.1.0     | rdkit-0.1.0-job.yaml               |
| ImageJ Plugin Converter | 0.1.0     | imagej-converter-0.1.0-job.yaml    |
| C++                     | 0.1.0     | cpp-0.1.0-job.yaml                 |
| Julia                   | 0.1.0     | julia-0.1.0-job.yaml               |
| Octave                  | 0.1.0     | octave-0.1.0-job.yaml              |
| Java                    | 1.8.0_312 | java-1.8.0_312-job.yaml            |
| Java                    | 11.0.3    | java-11.0.13-job.yaml              |
| Java                    | 17.0.1_12 | java-17.0.1_12-job.yaml            |
| Maven                   |           |                                    |
| JavaScript              | 0.1.0     | js-0.1.0-job.yaml                  |

- Maven

```

mkdir -p $EXT_MOD_PATH/maven-3.6.3
wget https://archive.apache.org/dist/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz
tar xvf apache-maven-3.6.3-bin.tar.gz -C $EXT_MOD_PATH/opt/modules/maven-3.6.3

```
