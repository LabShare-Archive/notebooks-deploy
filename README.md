[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)


# Notebooks Deploy

## Documentation

User documentation is available [here](docs/source/index.md).

## Setup

1. Clone the notebooks-deploy repository from GitHub using `git clone https://github.com/LabShare/notebooks-deploy`.
1. Install package dependencies using `npm i`.

## Development
### Running JupyterHub Locally
1. Create an .env file in your working directory. See the [sample-env](./sample-env) for an example. Docker-compose uses these environment variables to populate image and container arguments and environment variables. 
1. Build docker images using `npm run build`.
1. Start JupyterHub on `localhost:8000` using `npm start`.
1. JupyterHub is setup with DummyAuthenticator by default. Use any username or password to login.
1. To stop the running deployment use `npm run stop`.

## Deployment
### Kubernetes
1. Create a `.env` file in the root of the repository, using `sample-env` as an example.
1. Configure `kubectl` with a `kubeconfig` pointing to the correct Kubernetes cluster. Optionally, pass the location of the `kubeconfig` file in the `.env`. This value defaults to the standard `kubeconfig` location. 
1. Run the script using: `./deploy.sh`.

## CI and versioning

### Notebook image versioning
Modular notebook images are built in two steps: base image for a given VERSION: `labshare/polyglot-notebook:base-VERSION` and modular images built on top of base: `labshare/polyglot-notebook:HASH`. Base image contains package managers (conda, pip, etc), Jupyter and commonly used packages. Modular images contain additional packages and scripts to install, mainly to enable different Jupyter kernels and basic functionality for different programming languages. Modular images are built according to Dockerfile.template and collection of "stacks" - .yaml files containing dependencies to be included in modular images. Stacks are combined together and their dependencies are put in Dockerfile.template to create a working Docker build directory using the `polus-railyard` tool.

Both base and modular images are going to get built by CI when `deploy/docker/notebook/VERSION` is changed. VERSION is updated for any changes in either base or any of the stacks. Build will take a long time since there is a large number of stack combinations involved.

### Rolling out new version
The notebook version deployed is controlled separately through release tag and config variable `NOTEBOOK_VERSION_DEPLOY`. To deploy new version, you need to tag the commit where VERSION was changed with tag `notebook-x.y.z`, then update config variable `NOTEBOOK_VERSION_DEPLOY=notebook-x.y.z` and rerun the CI pipeline. Stacks from that tagged commit will now be mounted to the JupyterHub container.