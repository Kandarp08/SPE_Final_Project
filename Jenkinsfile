pipeline 
{
    agent any

    environment 
    {
        PROJECT_DIR = "${WORKSPACE}"
        VENV = "${WORKSPACE}/venv"
        PYTHON = "${VENV}/bin/python"
        PIP = "${VENV}/bin/pip"
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
                sh """
                . ${VENV}/bin/activate
                dvc pull
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

        stage("Start Minikube")
        {
            steps
            {
                script
                {
                    sh """
                    minikube start --preload=false
                    minikube status
                    """
                }
            }
        }

        stage("Deploy using Kubernetes")
        {
            steps
            {
                script
                {
                    sh """
                    kubectl apply -f ./kubernetes/namespace.yaml
                    kubectl apply -f ./kubernetes/deployment.yaml
                    kubectl apply -f ./kubernetes/service.yaml
                    kubectl apply -f ./kubernetes/ingress.yaml
                    """
                }
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
