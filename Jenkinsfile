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
        VERSION = "${env.BUILD_ID}"
        IMAGE_REPO = "sarthaksatish"
        NAMESPACE = "jenkins"
        HELM_CHART_DIRECTORY = "charts/priyankalearnings"
        //GITHUB_TOKEN = credentials('githubpat')
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
        stage('Clone/Pull Repo') {
            steps {
                script {
                    sh 'git clone https://github.com/sarsatis/helm-charts'
                    sh 'ls -ltr'
                }
            }
        }
        stage('Commit & Push') {
            steps {
                script {
                    dir("helm-charts/manifests/${NAME}/") {
                        withCredentials([usernamePassword(
                            credentialsId: 'githubpat',
                            usernameVariable: 'username',
                            passwordVariable: 'password'
                        )]) {
                            encodedPassword = URLEncoder.encode("$password", 'UTF-8')
                            echo "sa ${encodedPassword}"
                            sh "git config --global user.email 'jenkins@ci.com'"
                            sh "git remote set-url origin https://${username}:${encodedPassword}@github.com/${username}/helm-charts.git"
                            sh 'sed -i "s#tag:.*#tag: ${VERSION}#g" values.yaml'
                            sh 'cat values.yaml'
                            sh 'git add values.yaml'
                            sh 'git commit -am "Updated image version for Build - $VERSION"'
                            echo 'push started'
                            sh "git push -u origin main"
                        }
                        echo 'push complete'
                    }
                }
            }
        }
    }
}