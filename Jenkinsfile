pipeline {
    agent any 

    environment {
        auth_folder = "${WORKSPACE}"
        IMAGE_TAG_NAME = "authentication"
    }

    stages {
        stage('Docker Build') {
            steps{
                sh 'pwd'
                sh 'ls -la'
                // build docker image 
                sh "docker build -t auth ."
                // clean docker dangling image
                script {
                    try {
                        sh "docker rmi \$(docker images -f 'dangling=true' -q)"
                    } catch (Exception e) {
                        echo 'Exception occurred: ' + e.toString() 
                    } 
                } 
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
            }
        }
    }
    
}

