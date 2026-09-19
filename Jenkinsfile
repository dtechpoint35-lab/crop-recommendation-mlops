pipeline {

    agent any

    environment {
        APP_SERVER = "172.31.9.129"
        APP_USER = "ubuntu"
        DEPLOY_DIR = "/opt/crop-app"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Downloading project from GitHub...'
                checkout scm
            }
        }

        stage('Create Virtual Environment') {
            steps {
                echo 'Creating Python virtual environment...'

                sh '''
                    python3 -m venv venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'

                sh '''
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'

                sh '''
                    . venv/bin/activate
                    pytest tests/
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Deploying application to Flask server...'

                sh '''
                    ssh ${APP_USER}@${APP_SERVER} "
                        mkdir -p ${DEPLOY_DIR}
                    "

                    scp -r app \
                        ${APP_USER}@${APP_SERVER}:${DEPLOY_DIR}/

                    scp -r models \
                        ${APP_USER}@${APP_SERVER}:${DEPLOY_DIR}/

                    scp requirements.txt \
                        ${APP_USER}@${APP_SERVER}:${DEPLOY_DIR}/
                '''
            }
        }

        stage('Install Production Dependencies') {
            steps {
                echo 'Installing dependencies on Flask server...'

                sh '''
                    ssh ${APP_USER}@${APP_SERVER} "
                        cd ${DEPLOY_DIR}

                        if [ ! -d venv ]; then
                            python3 -m venv venv
                        fi

                        . venv/bin/activate

                        pip install --upgrade pip
                        pip install -r requirements.txt
                    "
                '''
            }
        }

        stage('Restart Flask Application') {
            steps {
                echo 'Restarting Flask application...'

                sh '''
                    ssh ${APP_USER}@${APP_SERVER} "
                        sudo systemctl restart crop-app
                    "
                '''
            }
        }
    }

    post {

        success {
            echo 'CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'CI/CD Pipeline failed!'
        }
    }
}