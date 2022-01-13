#!/usr/bin/env bash

source .env

# Backup file extension required to support Mac versions of sed
sed -i.bak \
    -e "s/STORAGE_CLASS_VALUE/${STORAGE_CLASS}/g" \
    deploy/kubernetes/postgres.yaml
rm deploy/kubernetes/postgres.yaml.bak

sed -i.bak \
    -e "s/SHARED_STORAGE_VALUE/${SHARED_STORAGE}/g" \
    -e "s/MODULES_STORAGE_VALUE/${MODULES_STORAGE}/g" \
    -e "s/STORAGE_CLASS_VALUE/${STORAGE_CLASS}/g" \
    deploy/kubernetes/storage.yaml
rm deploy/kubernetes/storage.yaml.bak

sed -i.bak \
    -e "s/NOTEBOOK_VERSION_DEPLOY_VALUE/${NOTEBOOK_VERSION_DEPLOY}/g" \
    -e "s/STORAGE_CLASS_VALUE/${STORAGE_CLASS}/g" \
    -e "s/STORAGE_PER_USER_VALUE/${STORAGE_PER_USER}/g" \
    -e "s/WIPP_STORAGE_PVC_VALUE/${WIPP_STORAGE_PVC}/g" \
    -e "s|WIPP_UI_VALUE|${WIPP_UI}|g" \
    -e "s|WIPP_API_INTERNAL_VALUE|${WIPP_API_INTERNAL}|g" \
    -e "s|WIPP_NOTEBOOKS_PATH_VALUE|${WIPP_NOTEBOOKS_PATH}|g" \
    -e "s|WIPP_PLUGIN_TEMP_PATH_VALUE|${WIPP_PLUGIN_TEMP_PATH}|g" \
    -e "s|POLUS_NOTEBOOKS_HUB_API_VALUE|${POLUS_NOTEBOOKS_HUB_API}|g" \
    -e "s|POLUS_NOTEBOOKS_HUB_FILE_LOGGING_ENABLED_VALUE|${POLUS_NOTEBOOKS_HUB_FILE_LOGGING_ENABLED}|g" \
    deploy/kubernetes/jupyterhub-configs.yaml
rm deploy/kubernetes/jupyterhub-configs.yaml.bak

CONFIG_HASH=$(shasum deploy/kubernetes/jupyterhub-configs.yaml | cut -d ' ' -f 1 | tr -d '\n')

sed -i.bak \
    -e "s/HUB_VERSION_VALUE/${HUB_VERSION}/g" \
    -e "s/CONFIG_HASH_VALUE/${CONFIG_HASH}/g" \
    deploy/kubernetes/jupyterhub-deployment.yaml
rm deploy/kubernetes/jupyterhub-deployment.yaml.bak

sed -i.bak \
    -e "s/NOTEBOOK_VERSION_LATEST_VALUE/${NOTEBOOK_VERSION_LATEST}/g" \
    deploy/docker/env-installer/Dockerfile
rm deploy/docker/env-installer/Dockerfile.bak

sed -i.bak \
    -e "s|JUPYTERHUB_URL_VALUE|${JUPYTERHUB_URL}|g" \
    deploy/kubernetes/jupyterhub-ingress.yaml
rm deploy/kubernetes/jupyterhub-ingress.yaml.bak

sed -i.bak \
    -e "s|JUPYTERHUB_URL_VALUE|${JUPYTERHUB_URL}|g" \
    deploy/kubernetes/jupyterhub-ingress.yaml
rm deploy/kubernetes/jupyterhub-ingress.yaml.bak


kubectl apply --kubeconfig=${KUBECONFIG} -f deploy/kubernetes/postgres.yaml
kubectl apply --kubeconfig=${KUBECONFIG} -f deploy/kubernetes/jupyterhub-predefined.yaml
kubectl apply --kubeconfig=${KUBECONFIG} -f deploy/kubernetes/storage.yaml
kubectl apply --kubeconfig=${KUBECONFIG} -f deploy/kubernetes/jupyterhub-configs.yaml
kubectl apply --kubeconfig=${KUBECONFIG} -f deploy/kubernetes/jupyterhub-services.yaml
kubectl apply --kubeconfig=${KUBECONFIG} -f deploy/kubernetes/jupyterhub-deployment.yaml
kubectl apply --kubeconfig=${KUBECONFIG} -f deploy/kubernetes/jupyterhub-ingress.yaml
kubectl apply --kubeconfig=${KUBECONFIG} -f deploy/kubernetes/env-installer.yaml