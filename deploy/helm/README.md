## Test deployment

For a simple testing, you can use the following chart values to simplify and remove most of the complexity.

```
hub:
    storageClass: aws-efs
    service:
        type: LoadBalancer
    ingress:
        enabled: false
    wipp:
        enabled: false
    polusNotebooksHub:
        enabled: false
postgresql:
  enabled: true
```

## Production deployment

### Configure ingress

### Configure LS Auth

Make sure that LS Auth redirect URL is pointing to ingress URL

## Environment Modules installation

Following the install or upgrade of the Helm Chart, you have the option to run the Helm Hooks to install the environment modules to enable different kernels for users. This chart provides a set of modules created for testing and internal use, but it is possible to modify those or create your own.

| Kernel              | Key name in hub.envModules | Version   |
| ------------------- | -------------------------- | --------- |
| Python Data Science | `pythonDataScience`        | 0.1.1     |
| R                   | `r`                        | 0.1.0     |
| Chemoinformatics    | `rdkit`                    | 0.1.0     |
| PyImageJ            | `pyimagej`                 | 0.1.0     |
| C++                 | `cpp`                      | 0.1.0     |
| Julia               | `julia`                    | 0.1.0     |
| Octave              | `octave`                   | 0.1.0     |
| Java                | `java`                     | 1.8.0_312 |
| Java                | `java`                     | 11.0.3    |
| Java                | `java`                     | 17.0.1_12 |
| Maven               | `maven`                    | 3.6.3     |
| JavaScript          | `js`                       | 0.1.0     |

The installation of environment modules is performed using K8s Jobs and configMaps. ConfigMap allows to provide the context for the installer, i.e. conda environment definitions and modulefiles, whereas the Job lists the environment variables specifiying the metadata, i.e. the version of the environment module to be installed, as well as the shell commands requied to install the environment module to the shared modules volume.

When using the provided installer from the table above, just add the corresponding key and version number like so:

```
hub:
  envModules:
    <key>:
      - <version>
```

You may install multiple versions at the same time

```
hub:
  envModules:
    <key>:
      - <version1>
      - <version2>
```

Keep in mind that installation make take a while, i.e. when it includes Conda environment solving. Please add a timeout key to you Helm CLI command: `--timeout 2h`.
