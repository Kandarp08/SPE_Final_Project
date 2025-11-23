pipeline {
    agent any

    environment 
    {
        PROJECT_DIR = "${WORKSPACE}"
        VENV = "${WORKSPACE}/venv"
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
                    source ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        // stage("Preprocess Data") 
        // {
        //     steps 
        //     {
        //         sh """
        //             source ${VENV}/bin/activate
        //             python3 src/preprocess.py
        //         """
        //     }
        // }

        // stage("Train Model") 
        // {
        //     steps 
        //     {
        //         sh """
        //             source ${VENV}/bin/activate
        //             python3 src/train.py
        //         """
        //     }
        // }

        // stage("Evaluate Model") 
        // {
        //     steps {
        //         sh """
        //             source ${VENV}/bin/activate
        //             python3 src/test.py
        //         """
        //     }
        // }
    }

    post 
    {
        success 
        {
            echo "Pipeline completed successfully."
        }

        failure 
        {
            echo "Pipeline Failed."
        }
    }
}
