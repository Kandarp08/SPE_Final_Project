pipeline 
{
    agent any

    environment 
    {
        PROJECT_DIR = "${WORKSPACE}"
        VENV = "${WORKSPACE}/venv"
        PYTHON = "${VENV}/bin/python"
        PIP = "${VENV}/bin/pip"

        MLFLOW_DB_PATH        = "/var/lib/jenkins/mlflow_db"
        MLFLOW_ARTIFACT_PATH  = "/var/lib/jenkins/mlflow_artifacts"
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

        stage("Setup Kaggle Credentials") 
        {
            steps 
            {
                withCredentials([file(credentialsId: 'KAGGLE_API_TOKEN', variable: 'KAGGLE_FILE')]) {
                    sh """
                    mkdir -p ~/.kaggle
                    cp $KAGGLE_FILE ~/.kaggle/kaggle.json
                    chmod 600 ~/.kaggle/kaggle.json
                    """
                }
            }
        }

        stage("Prepare MLflow Storage") 
        {
            steps 
            {
                sh """
                    sudo mkdir -p $MLFLOW_DB_PATH
                    sudo mkdir -p $MLFLOW_ARTIFACT_PATH

                    sudo chown -R jenkins:jenkins $MLFLOW_DB_PATH
                    sudo chown -R jenkins:jenkins $MLFLOW_ARTIFACT_PATH
                """
            }
        }

        stage("Pull Data (DVC)") 
        {
            steps 
            {
                sh """
                . ${VENV}/bin/activate
                dvc pull -v
                """
            }
        }

        stage("Run Pipeline (DVC)") 
        {
            steps 
            {
                sh """
                . ${VENV}/bin/activate
                dvc repro
                """
            }
        }

        stage("Push Artifacts (DVC)") 
        {
            steps 
            {
                sh """
                . ${VENV}/bin/activate
                dvc push
                """
            }
        }

        stage("Build Docker Image") 
        {
            steps 
            {
                script
                {
                    docker.build("kandarp53/diabetes_prediction:latest")
                }
            }
        }

        stage("Push to DockerHub") 
        {
            steps 
            {
                script
                {
                    docker.withRegistry("https://index.docker.io/v1/", "dockerhub-credentials") {
                        docker.image("kandarp53/diabetes_prediction:latest").push()
                    }
                }
            }
        }

        stage("Deploy to Kubernetes using Ansible") 
        {
            steps 
            {
                sh """
                . ${VENV}/bin/activate
                ansible-playbook -i ansible/inventory.ini ansible/deployment.yml
                """
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
