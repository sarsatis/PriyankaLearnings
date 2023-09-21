def podTemplate = "podTemplate.yaml"

pipeline {
    agent {
        kubernetes {
            label "jenkins-${UUID.randomUUID().toString()}"
            yamlFile "$podTemplate"
        }
    }
    environment {
        NAME = "priyankalearnings"
        // VERSION = "${env.GIT_COMMIT}"
        VERSION = "${env.BUILD_ID}"
        IMAGE_REPO = "sarthaksatish"
        NAMESPACE = "jenkins"
        HELM_CHART_DIRECTORY = "charts/priyankalearnings"
        GITHUB_TOKEN = credentials('githubpat')
    }
    stages {
        stage('Unit Tests') {
            steps {
                echo 'Implement unit tests if applicable.'
                echo 'This stage is a sample placeholder'
            }
        }
        stage('Gradle build') {
            steps {
                script {
                    container(name: 'gradle') {
                        sh "gradle clean build"
                    }
                }
            }
        }
        stage('Build Image') {
            steps {
                script {
                    container('kaniko') {
                        sh '''
              /kaniko/executor --context `pwd` --destination ${IMAGE_REPO}/${NAME}:${VERSION}
            '''
                    }
                }
            }
        }
        // stage('helm install') {
        //   steps {
        //     script{
        //         container('helm'){
        //           sh "helm list"
        //           sh "helm lint ./${HELM_CHART_DIRECTORY}"
        //           sh "helm upgrade --set image.tag=${VERSION} ${NAME} ./${HELM_CHART_DIRECTORY} -n ${NAMESPACE}"
        //           sh "helm list"
        //         }
        //          }
        //     }
        //   }
        // stage('Clone/Pull Repo') {
        //     steps {
        //         script {
        //             if (fileExists('helm-charts')) {
        //                 echo 'Cloned repo already exists - Pulling latest changes'
        //                 dir("helm-charts") {
        //                     sh 'git pull'
        //                 }
        //             } else {
        //                 sh 'git clone https://github.com/sarsatis/helm-charts'
        //                 sh 'ls -ltr'
        //             }
        //         }
        //     }
        // }
        // stage('Commit & Push') {
        //     steps {
        //         script {
        //             dir("helm-charts/manifests/${NAME}/") {
        //                 withCredentials([usernamePassword(
        //                     credentialsId: 'githubpat',
        //                     usernameVariable: 'username',
        //                     passwordVariable: 'password'
        //                 )]) {
        //                     encodedPassword = URLEncoder.encode("$password", 'UTF-8')
        //                     echo "sa ${encodedPassword}"
        //                     sh "git config --global user.email 'jenkins@ci.com'"
        //                     sh "git remote set-url origin https://${username}:${encodedPassword}@github.com/${username}/helm-charts.git"
        //                     sh 'sed -i "s#tag:.*#tag: ${VERSION}#g" values-dev.yaml'
        //                     sh "git checkout -b ${NAME}-${env.BUILD_ID}"
        //                     sh 'cat values-dev.yaml'
        //                     sh 'git add values-dev.yaml'
        //                     sh 'git commit -am "Updated image version for Build - $VERSION"'
        //                     echo 'push started'
        //                     sh "git push origin ${NAME}-${env.BUILD_ID}"
        //                 }
        //                 echo 'push complete'
        //             }
        //         }
        //     }
        // }

        stage('Raise PR') {
          steps {
             script {
                withCredentials([usernamePassword(credentialsId: 'githubpat',
                      usernameVariable: 'username',
                      passwordVariable: 'password')]){
                    encodedPassword = URLEncoder.encode("$password",'UTF-8')
                    echo 'In Pr'
                    container(name: 'python') {
                    sh "printenv"
                    sh "pip3 install -r requirements.txt"
                    //sh "python3 oop.py"
                    sh "python3 createprandaddlabels.py"
                    }
                      }
                // sh "bash pr.sh"
            }
          }
        }
    }
}
