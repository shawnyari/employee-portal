pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t employee-portal:latest .'
            }
        }

        stage('Deploy Employee Portal') {
            steps {
                sh '''
                    docker rm -f employee-portal || true
                    docker run -d --name employee-portal -p 8081:80 employee-portal:latest
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'curl -f http://localhost:8081'
            }
        }
    }
}
