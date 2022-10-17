pipeline {
    agent any 

    environment {
        auth_folder = "${WORKSPACE}"
        IMAGE_TAG_NAME = "authentication"
    }

    stages {
        stage('Docker Build') {
            steps{
                // build docker image 
                sh "docker build -t auth ."
            }
        } 

        stage('Push image to docker hub') {
            steps {
                script {
                    
                    docker.withRegistry('', 'dockerHub-access' ) {
                        def customImage = docker.build("yaradata/$IMAGE_TAG_NAME:latest")
                        customImage.push()

                        // docker push yaradata/authentication:tagname

                        // docker tag local-image:tagname new-repo:tagname
                        // docker push new-repo:tagname
                    }

                }
            }
        }
        
        stage('Kubernetes Deploy') {
            steps{
                echo "deploy" 
                sh "docker run -itd -p 4114:8000 --name auth yaradata/$IMAGE_TAG_NAME:latest"
            }
        }
    }
    
}

