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
                dvc repro --force download_data
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
                    minikube start \
                    --driver=docker \
                    --preload=false \
                    --force \
                    --interactive=false

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
                    kubectl delete ValidatingWebhookConfiguration ingress-nginx-admission
                    kubectl apply --validate=false -f ./kubernetes/ingress.yaml
                    """
                }
            }
        }

        stage("Apply ELK stack")
        {
            steps
            {
                script
                {
                    sh """
                    docker-compose -f ./elk-stack/docker-compose.yml up -d
                    kubectl apply -f ./kubernetes/fluent-bit/
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
