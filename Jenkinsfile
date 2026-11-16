pipeline {
    agent any

    environment {
        PYTHON_EXE = 'C:\\Users\\LENOVO\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe'
    }

    triggers {
        pollSCM('* * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/ShreyanshuRaj06/devops-task-api.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"%PYTHON_EXE%" -m pip install -r requirements.txt'
            }
        }

        stage('Run Automated Tests (CI Enhancement)') {
            steps {
                bat '"%PYTHON_EXE%" -m pytest -v'
            }
        }

        stage('Package Build Artifact') {
            steps {
                bat '''
                    if not exist dist mkdir dist
                    powershell -Command "Compress-Archive -Path app.py,requirements.txt,test_app.py -DestinationPath dist\\devops-task-api-build-%BUILD_NUMBER%.zip -Force"
                '''
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'dist/*.zip', fingerprint: true
        }
    }
}