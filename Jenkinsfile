pipeline{
    agennt any 

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                echo 'Cloning Github repo to Jenkins...........'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'Github-token', url: 'https://github.com/shubhambagalsrb/MLOPS-COURSE-PROJECT-1.git']])
                }
            }
        }
    }
}