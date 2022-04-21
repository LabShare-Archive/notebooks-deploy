[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)

# Notebooks Deploy

## Documentation

User documentation is available [here](docs/source/index.md).

## Docker images

Applications are packaged as Docker containers. There are currently the following images in the repo

- JupyterHub
- Notebook
- Environment Module Installer
- Docs

### Automatic builds

Dockere images are automatically built in Github Actions every time the corresponding `VERSION` file is changed.

### Notebook image versioning

JupyterLab server Docker images are built for a given semantic `VERSION=major.minor.patch`: `labshare/polyglot-notebook:VERSION`. Notebook image contains package managers (conda, pip, etc), Jupyter and some essential packages. Starting with VERSION=0.9.0 all software dependencies and various Jupyter kernels for running notebook cells are provided by environment modules (Lmod), which are built and installed separately on a mounted volume.

## Helm Deployment

### Minimal test deployemnt

To test the basic functionality of the application (for example using Docker Desktop K8s functionality or a separate namespace on cluster), you can select the minimal viable configuration without auth, persistent database and any other integrations enabled

1. Create `local-values.yaml` with the following content

```yaml
hub:
  storage:
    storageClass: aws-efs
    storagePerUser: 1Gi
    sharedNotebooksStorage: 1Gi
    modulesStorage: 1Gi

  service:
    type: NodePort

postgresql:
  enabled: false
```

2. Install chart dependencies

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm dependency update
helm dependency build
```

3. Deploy the application `helm upgrade --install --generate-name deploy/helm --values local-values.yaml --namespace ${KUBERNETES_NAMESPACE}`

### CI deployment with Jenkins

CI deployment is similar to the above, with following differences:

- Helm values are stored in Jenkins config file (jupyterhub-helm-values)
- Installation is automatic

#### Rolling out new version

- To update JupyterHub, change the version in `hub.image.tag`
- To update Notebook, change the version in `hub.notebookVersion`

Submit configuration file and rerun the CI pipeline.
