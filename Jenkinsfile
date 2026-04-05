pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "project-bd45127e-4197-40d2-b33"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Github-token', url: 'https://github.com/shubhambagalsrb/MLOPS-COURSE-PROJECT-1.git']])
                }
            }
        }

        stage('Setting up our Virtual Environment and Installing dependancies'){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Installing dependancies............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Building and Pushing Docker Image to GCR'){
    steps{
        script{
                    echo 'Building and Pushing Docker Image to GCR (WIF).............'
                    sh '''
                    export PATH=$PATH:${GCLOUD_PATH}
                    export GOOGLE_EXTERNAL_ACCOUNT_ALLOW_EXECUTABLES=1
                    export GOOGLE_APPLICATION_CREDENTIALS=/var/jenkins_home/credentials.json

                    gcloud auth login --cred-file=$GOOGLE_APPLICATION_CREDENTIALS

                    gcloud config set project ${GCP_PROJECT}
                    gcloud auth configure-docker --quiet
                    docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                    docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                    '''
                }
            }
        }


        stage('Deploy to Google Cloud Run'){
            steps{
                script{
                    echo 'Deploy to Google Cloud Run.............'
                    sh '''
                    export PATH=$PATH:${GCLOUD_PATH}
                    export GOOGLE_APPLICATION_CREDENTIALS=/var/jenkins_home/credentials.json

                    # Authenticate using WIF
                    gcloud auth login --cred-file=$GOOGLE_APPLICATION_CREDENTIALS


                    gcloud config set project ${GCP_PROJECT}

                    gcloud run deploy ml-project \
                        --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
                        --platform=managed \
                        --region=us-central1 \
                        --allow-unauthenticated
                    '''
                }
            }
        }
        
    }
}