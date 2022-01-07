pipeline {
    agent {
        node { label 'aws && ci && linux && polus' }
    }
    options { timestamps () }
    parameters {
        booleanParam(name: 'SKIP_BUILD', defaultValue: false, description: 'Skips Docker builds')
	string(name: 'AWS_REGION', defaultValue: 'us-east-1', description: 'AWS Region to deploy')
	string(name: 'KUBERNETES_CLUSTER_NAME', defaultValue: 'kube-eks-ci-compute', description: 'Kubernetes Cluster to deploy')
    }
    environment {
        PROJECT_NAME = "labshare/notebooks-deploy"
        DOCKER_CLI_EXPERIMENTAL = "enabled"
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
        stage('Assemble Jupyter Notebook Dockerfiles') {
            when {
                environment name: 'SKIP_BUILD', value: 'false'
                environment name: 'BUILD_NOTEBOOK', value: '0'
            }
            agent {
                docker {
                    image 'labshare/polus-railyard:0.3.2'
                    registryUrl 'https://registry-1.docker.io/v2/'
                    registryCredentialsId 'f16c74f9-0a60-4882-b6fd-bec3b0136b84'
                    args '--network=host'
                    reuseNode true
                }
            }
            steps {
                script {
                    dir('deploy/docker/notebook') {
                        withEnv(["HOME=${env.WORKSPACE}"]) {
                            sh 'mkdir -p manifests'

                            stacks = [
                                'java.yaml', 
                                'scala.yaml',
                                'latex.yaml'
                            ]

                            // CPU-based image
                            sh "railyard assemble -t Dockerfile.template -b base.yaml " + stacks.collect{"-a " + it}.join(" ") + " -p manifests"
                            // GPU-based image
                            // sh "railyard assemble -t Dockerfile.template -b base-gpu.yaml " + stacks.collect{"-a " + it}.join(" ") + " -p manifests"
                        }
                    }
                }
            }
        }
        stage('Build Jupyter Notebook Docker images') {
            when {
                environment name: 'SKIP_BUILD', value: 'false'
                environment name: 'BUILD_NOTEBOOK', value: '0'
            }
            steps {
                script {
                    sh """echo '{"experimental": "enabled"}' > ~/config.json"""
                    dir('deploy/docker/notebook/manifests') {
                        def files = findFiles(glob: '**/Dockerfile')
                        files.each {
                            def hash = it.path.minus(it.name).minus('/')
                            def tag = NOTEBOOK_VERSION

                            dir("""${hash}""") {
                                docker.withRegistry('https://registry-1.docker.io/v2/', 'f16c74f9-0a60-4882-b6fd-bec3b0136b84') {
                                    println """Building container image: labshare/polyglot-notebook:${tag}..."""
                                    def image = docker.build("""labshare/polyglot-notebook:${tag}""", '--no-cache ./')
                                    println """Pushing container image: ${tag}..."""
                                    image.push()
                                }
                            }
                            println """Clean Docker cache to save disk"""
                            sh """docker system prune -a -f"""
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
        stage('Deploy JupyterHub to AWS CI') {
            steps {
                // Config JSON file is stored in Jenkins and should contain sensitive environment values.
                configFileProvider([configFile(fileId: 'env-ci', targetLocation: '.env')]) {               
                    withAWS(credentials:'aws-jenkins-eks') {
                        sh "aws --region ${AWS_REGION} eks update-kubeconfig --name ${KUBERNETES_CLUSTER_NAME}"

                        sh "bash ./deploy.sh"
                    }
                }
            }
        }
        // stage('Deploy JupyterHub to NCATS') {
        //     agent {
        //         node { label 'ls-api-ci.ncats' }
        //     }
        //     steps {
        //         configFileProvider([configFile(fileId: 'env-single-node', targetLocation: '.env')]) {
        //             withKubeConfig([credentialsId: 'ncats_polus2']) {
        //                 sh "bash ./deploy.sh"
        //             }
        //         }
        //     }
        // }
    }
    post {
        always {
            script {
                cleanWs()
                sh 'docker system prune -a -f'
            }
        }
    }
}
