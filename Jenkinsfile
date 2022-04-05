pipeline {
    agent {
        node { label 'aws && build && linux && ubuntu' }
    }
    options { timestamps () }
    parameters {
        string(name: 'AWS_REGION', defaultValue: 'us-east-1', description: 'AWS Region to deploy')
        string(name: 'KUBERNETES_CLUSTER_NAME', defaultValue: 'kube-eks-ci-compute', description: 'Kubernetes Cluster to deploy')
    }
    environment {
        PROJECT_NAME = "labshare/notebooks-deploy"
    }
    triggers {
        pollSCM('H/5 * * * *')
    }
    stages {
        stage('Checkout source code') {
            steps {
                cleanWs()
                checkout scm
            }
        }
        stage('Deploy JupyterHub to AWS CI') {
            steps {
                dir('deploy/helm') {
                    // Helm values are stored in yaml file in Jenkins
                    configFileProvider([configFile(fileId: 'jupyterhub-helm-values', targetLocation: 'ci-values.yaml')]) {               
                        withAWS(credentials:'aws-jenkins-eks') {
                            sh "aws --region ${AWS_REGION} eks update-kubeconfig --name ${KUBERNETES_CLUSTER_NAME}"
                            sh "helm install . --values ci-values.yaml --generate-name --dry-run --namespace polus-helm-sandbox"
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            script {
                cleanWs()
            }
        }
    }
}
