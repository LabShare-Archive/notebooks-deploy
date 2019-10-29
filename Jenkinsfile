pipeline {
    agent {
        node { label 'linux && build && aws' }
    }
    parameters {
        booleanParam(name: 'SKIP_BUILD', defaultValue: false, description: 'Skips Docker builds')
	string(name: 'AWS_REGION', defaultValue: 'us-east-1', description: 'AWS Region to deploy')
	string(name: 'KUBERNETES_CLUSTER_NAME', defaultValue: 'kube-eks-ci-compute', description: 'Kubernetes Cluster to deploy')
    }
    environment {
        PROJECT_NAME = "labshare/notebooks-deploy"
        BUILD_HUB = """${sh (
            script: "git diff --name-only ${GIT_PREVIOUS_SUCCESSFUL_COMMIT} ${GIT_COMMIT} | grep 'jupyterhub/VERSION'",
            returnStatus: true
        )}"""
        BUILD_NOTEBOOK = """${sh (
            script: "git diff --name-only ${GIT_PREVIOUS_SUCCESSFUL_COMMIT} ${GIT_COMMIT} | grep 'notebook/VERSION'",
            returnStatus: true
        )}"""
        BUILD_DOCS = """${sh (
            script: "git diff --name-only ${GIT_PREVIOUS_SUCCESSFUL_COMMIT} ${GIT_COMMIT} | grep 'docs/VERSION'",
            returnStatus: true
        )}"""
        HUB_VERSION = readFile(file: 'deploy/docker/jupyterhub/VERSION')
        NOTEBOOK_VERSION = readFile(file: 'deploy/docker/notebook/VERSION')
        DOCS_VERSION = readFile(file: 'deploy/docker/docs/VERSION')
        STORAGE_PER_USER = "1Gi"
        STORAGE_CLASS = "rook-cephfs"
        SHARED_STORAGE = "5Gi"
        WIPP_STORAGE_PVC = "wipp-pv-claim"
    }
    triggers {
        pollSCM('H/5 * * * *')
    }
    stages {
        stage('Build Version'){
            steps{
                script {
                    BUILD_VERSION_GENERATED = VersionNumber(
                        versionNumberString: 'v${BUILD_YEAR, XX}.${BUILD_MONTH, XX}${BUILD_DAY, XX}.${BUILDS_TODAY}',
                        projectStartDate:    '1970-01-01',
                        skipFailedBuilds:    true)
                    currentBuild.displayName = BUILD_VERSION_GENERATED
                    env.BUILD_VERSION = BUILD_VERSION_GENERATED
               }
            }
        }
        stage('Checkout source code') {
            steps {
                cleanWs()
                checkout scm
            }
        }
        stage('Build JupyterHub Docker') {
            when {
                environment name: 'SKIP_BUILD', value: 'false'
                environment name: 'BUILD_HUB', value: '0'
            }
            steps {
                script {
                    dir('deploy/docker/jupyterhub') {
                        docker.withRegistry('https://registry-1.docker.io/v2/', 'f16c74f9-0a60-4882-b6fd-bec3b0136b84') {
                            def image = docker.build('labshare/jupyterhub:latest', '--no-cache ./')
                            image.push()
                            image.push(env.HUB_VERSION)
                        }
                    }
                }
            }
        }
        stage('Build Jupyter Notebook Docker') {
            when {
                environment name: 'SKIP_BUILD', value: 'false'
                environment name: 'BUILD_NOTEBOOK', value: '0'
            }
            steps {
                script {
                    dir('deploy/docker/notebook') {
                        docker.withRegistry('https://registry-1.docker.io/v2/', 'f16c74f9-0a60-4882-b6fd-bec3b0136b84') {
                            def image = docker.build('labshare/polyglot-notebook:latest', '--no-cache ./')
                            image.push()
                            image.push(env.NOTEBOOK_VERSION)
                        }
                    }
                }
            }
        }
        stage('Build Notebooks documentation') {
            when {
                environment name: 'SKIP_BUILD', value: 'false'
                environment name: 'BUILD_DOCS', value: '0'
            }
            steps {
                script {
                    sh "mv docs/* deploy/docker/docs"
                    dir('deploy/docker/docs') {
                        docker.withRegistry('https://registry-1.docker.io/v2/', 'f16c74f9-0a60-4882-b6fd-bec3b0136b84') {
                            def image = docker.build('labshare/notebook-docs:latest', '--no-cache ./')
                            image.push()
                            image.push(env.DOCS_VERSION)
                        }
                    }
                }
            }
        }
        stage('Deploy JupyterHub to Kubernetes') {
            steps {
                dir('deploy/kubernetes') {
                    configFileProvider([configFile(fileId: 'env-ci', targetLocation: 'env-ci.json')]) {
                        script {
                            def urls = readJSON file: 'env-ci.json'
                            
                            sh "sed -i 's/SHARED_STORAGE_VALUE/${SHARED_STORAGE}/g' storage.yaml"
                            sh "sed -i 's/STORAGE_CLASS_VALUE/${STORAGE_CLASS}/g' storage.yaml"
                            sh "sed -i 's/NOTEBOOK_VERSION_VALUE/${NOTEBOOK_VERSION}/g' jupyterhub-configs.yaml"
                            sh "sed -i 's/STORAGE_PER_USER_VALUE/${STORAGE_PER_USER}/g' jupyterhub-configs.yaml"
                            sh "sed -i 's/WIPP_STORAGE_PVC_VALUE/${WIPP_STORAGE_PVC}/g' jupyterhub-configs.yaml"
                            sh "sed -i 's|WIPP_UI_NOTEBOOKS_VALUE|${urls.wipp_ui_notebooks}|g' jupyterhub-configs.yaml"
                            sh "sed -i 's/HUB_VERSION_VALUE/${HUB_VERSION}/g' jupyterhub-deployment.yaml"
                            sh "sed -i 's|JUPYTERHUB_URL_VALUE|${urls.jupyterhub_url}|g' jupyterhub-services.yaml"

                            // Calculate config hash after substitution to connect configuration changes to deployment
                            env.CONFIG_HASH = sh(script: "shasum jupyterhub-configs.yaml | cut -d ' ' -f 1 | tr -d '\n'", returnStdout: true)

                            sh "sed -i 's/CONFIG_HASH_VALUE/${CONFIG_HASH}/g' jupyterhub-deployment.yaml"
                        }
                    }
                    
                    withAWS(credentials:'aws-jenkins-eks') {
                        sh "aws --region ${AWS_REGION} eks update-kubeconfig --name ${KUBERNETES_CLUSTER_NAME}"

                        sh '''
                            kubectl apply -f storage.yaml
                            kubectl apply -f jupyterhub-configs.yaml
                            kubectl apply -f jupyterhub-services.yaml
                            kubectl apply -f jupyterhub-deployment.yaml
                        '''
                    }
                }
            }
        }
    }
}
