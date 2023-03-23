def podTemplate = "podTemplate.yaml"

pipeline {
  agent {
    kubernetes{
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

    stage('Gradle build'){
      steps{
        script{
        container(name: 'gradle'){
           sh "gradle clean build"
        }
        }
      }

    }

    stage('Build Image') {
      steps {
        script{
            container('kaniko'){
              sh '''
              /kaniko/executor --context `pwd` --destination ${IMAGE_REPO}/${NAME}:${VERSION}
            '''
            }
             }
        }
      }
    
    stage('helm install') {
      steps {
        script{
            container('helm'){
              sh "helm list"
              sh "helm lint ./${HELM_CHART_DIRECTORY}"
              sh "helm upgrade --set image.tag=${VERSION} ${NAME} ./${HELM_CHART_DIRECTORY} -n ${NAMESPACE}"
              sh "helm list"
            }
             }
        }
      }
  }
}