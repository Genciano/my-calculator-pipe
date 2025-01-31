pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = 'dockerhub-credential' // ID das credenciais Docker
        GIT_CREDENTIALS = 'github-credential' // ID das credenciais GitHub
        KUBE_CONFIG = 'minikube-credential' // ID das credenciais Kubernetes
        DOCKER_IMAGE = 'genciano/my-calculator-pipe'
        K8S_NAMESPACE = 'default' // Substitua se necessário
    }

    stages {
        stage('Clonar Repositório') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/master']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Genciano/my-calculator-pipe.git',
                        credentialsId: GIT_CREDENTIALS
                    ]]
                ])
            }
        }

        stage('Build da Imagem Docker') {
            steps {
                script {
                    sh '''
                    docker build -t $DOCKER_IMAGE:latest .
                    '''
                }
            }
        }

        stage('Push para o Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $DOCKER_IMAGE:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy no Kubernetes com Helm') {
            steps {
                withCredentials([file(credentialsId: KUBE_CONFIG, variable: 'KUBECONFIG')]) {
                    script {
                        sh '''
                        helm upgrade --install my-app ./my-calculator-chart \
                            --set image.repository=$DOCKER_IMAGE \
                            --set image.tag=latest \
                            --namespace $K8S_NAMESPACE
                        '''
                    }
                }
            }
        }
    }
}
