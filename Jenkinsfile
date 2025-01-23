pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'seu-usuario-dockerhub' // Substitua pelo seu usuário Docker Hub
        IMAGE_NAME = 'minha-aplicacao'           // Nome da imagem no Docker Hub
        KUBE_CONFIG_PATH = '/root/.kube/config' // Caminho do kubeconfig dentro do container Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-login', 
                    usernameVariable: 'DOCKER_USERNAME', 
                    passwordVariable: 'DOCKER_PASSWORD'
                )]) {
                    script {
                        sh "echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USERNAME} --password-stdin"
                        sh "docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest"
                    }
                }
            }
        }

        stage('Deploy with Helm') {
            steps {
                withKubeConfig([credentialsId: 'kubeconfig-minikube', kubeconfigId: 'minikube-config']) {
                    script {
                        sh """
                        helm upgrade --install my-app ./helm-chart/ \
                            --set image.repository=${DOCKER_REGISTRY}/${IMAGE_NAME} \
                            --set image.tag=latest
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed!'
        }
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}

