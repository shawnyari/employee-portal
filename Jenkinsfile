pipeline {
    agent any

    environment {
        IMAGE = 'yarishawn/employee-portal:latest'
        ANSIBLE_DIR = '/home/ubuntu/employee-portal-ansible'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push "$IMAGE"
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                sh '''
                    cd "$ANSIBLE_DIR"
                    ansible-playbook -i inventory.ini deploy-app.yml
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    cd "$ANSIBLE_DIR"
                    ansible -i inventory.ini app_servers -m shell -a "curl -fsS http://127.0.0.1:5000/api/health"
                '''
            }
        }
    }

    post {
        success {
            echo 'Employee Portal CI/CD Pipeline SUCCESS!'
        }
        failure {
            echo 'Employee Portal CI/CD Pipeline FAILED!'
        }
    }
}
