pipeline {
    agent any

    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['api', 'smoke', 'regression', 'ui', 'all'],
            description: 'pytest suite to run'
        )
        string(
            name: 'BASE_URL',
            defaultValue: 'http://localhost:8080/jpetstore',
            description: 'JPetStore base URL'
        )
    }

    environment {
        VENV_DIR = '.venv'
        ALLURE_RESULTS_DIR = 'automation/reports/ci/allure-results'
        ALLURE_RESULTS_ARG = 'reports/ci/allure-results'
    }

    stages {
        stage('Prepare Python Environment') {
            steps {
                bat 'python -m venv %VENV_DIR%'
                bat '%VENV_DIR%\\Scripts\\python.exe -m pip install --upgrade pip'
                bat '%VENV_DIR%\\Scripts\\python.exe -m pip install -r automation\\requirements.txt'
            }
        }

        stage('Run Automated Tests') {
            steps {
                bat '''
                if exist automation\\reports\\ci rmdir /s /q automation\\reports\\ci
                cd automation
                ..\\%VENV_DIR%\\Scripts\\python.exe run_tests.py --suite %TEST_SUITE% --base-url %BASE_URL% --allure-results-dir %ALLURE_RESULTS_ARG%
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'automation/reports/ci/allure-results/**', allowEmptyArchive: true
            script {
                try {
                    allure includeProperties: false, jdk: '', results: [[path: env.ALLURE_RESULTS_DIR]]
                } catch (Exception ignored) {
                    echo 'Allure Jenkins plugin is not available; archived raw Allure results instead.'
                }
            }
        }
    }
}
