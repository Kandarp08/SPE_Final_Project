pipeline 
{
    agent any

    environment 
    {
        PROJECT_DIR = "${WORKSPACE}"
        VENV = "${WORKSPACE}/venv"
        PYTHON = "${VENV}/bin/python"
        PIP = "${VENV}/bin/pip"
        DVC = "${VENV}/bin/dvc"
        MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"
    }

    stages 
    {
        stage("Checkout Code") 
        {
            steps 
            {
                checkout scm
            }
        }

        stage("Setup Python Environment") 
        {
            steps 
            {
                sh """
                    python3 -m venv ${VENV}
                    ${PIP} install --upgrade pip
                    ${PIP} install -r requirements.txt
                """
            }
        }

        stage("Pull Data + Models (DVC)") 
        {
            steps 
            {
                sh "${DVC} pull"
            }
        }

        stage("Run Pipeline (DVC)") 
        {
            steps 
            {
                sh "${DVC} repro"
            }
        }

        stage("Push Artifacts (DVC)") 
        {
            steps 
            {
                sh "${DVC} push"
            }
        }
    }

    post 
    {
        success 
        {
            echo "Pipeline completed successfully."
        }

        failure 
        {
            echo "Pipeline failed."
        }
    }
}
