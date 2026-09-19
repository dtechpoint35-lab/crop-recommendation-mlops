```groovy
pipeline {

    agent any

    environment {
        APP_SERVER = "172.31.9.129"
        APP_USER   = "ubuntu"
        DEPLOY_DIR = "/opt/crop-app"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Downloading project from GitHub...'

                // Jenkins already checks out the repository
                // No second checkout is required here.
                sh '''
                    echo "Project files:"
                    ls -la
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                echo 'Creating Python virtual environment...'

                sh '''
                    rm -rf venv
                    python3 -m venv venv

                    echo "Python version:"
                    venv/bin/python --version

                    echo "Pip version:"
                    venv/bin/pip --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'

                sh '''
                    venv/bin/pip install --upgrade pip

                    venv/bin/pip install -r requirements.txt

                    # pytest is required for CI testing
                    venv/bin/pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'

                sh '''
                    echo "Running pytest..."

                    venv/bin/pytest tests/ -v
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Deploying application to Flask server...'

                sh '''
                    echo "Creating deployment directory..."

                    ssh ${APP_USER}@${APP_SERVER} \
                        "mkdir -p ${DEPLOY_DIR}"

                    echo "Copying application files..."

                    scp -r app \
                        ${APP_USER}@${APP_SERVER}:${DEPLOY_DIR}/

                    echo "Copying models..."

                    scp -r models \
                        ${APP_USER}@${APP_SERVER}:${DEPLOY_DIR}/

                    echo "Copying requirements.txt..."

                    scp requirements.txt \
                        ${APP_USER}@${APP_SERVER}:${DEPLOY_DIR}/

                    echo "Deployment files copied successfully."

                    ssh ${APP_USER}@${APP_SERVER} \
                        "ls -la ${DEPLOY_DIR}"
                '''
            }
        }

        stage('Install Production Dependencies') {
            steps {
                echo 'Installing dependencies on Flask server...'

                sh '''
                    ssh ${APP_USER}@${APP_SERVER} "
                        set -e

                        cd ${DEPLOY_DIR}

                        echo 'Checking Python...'
                        python3 --version

                        echo 'Checking virtual environment...'

                        if [ ! -d venv ]; then
                            python3 -m venv venv
                        fi

                        echo 'Installing production dependencies...'

                        venv/bin/pip install --upgrade pip
                        venv/bin/pip install -r requirements.txt

                        echo 'Production dependencies installed.'
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
                        sudo systemctl status crop-app --no-pager
                    "
                '''
            }
        }
    }

    post {

        success {
            echo '=========================================='
            echo 'CI/CD Pipeline completed successfully!'
            echo 'Application deployed successfully!'
            echo '=========================================='
        }

        failure {
            echo '=========================================='
            echo 'CI/CD Pipeline failed!'
            echo 'Check the stage above for the error.'
            echo '=========================================='
        }
    }
}
```
