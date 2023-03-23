def podTemplate = "podTemplate.yaml"

pipeline {
  agent {
    kubernetes{
      label "jenkins-${UUID.randomUUID().toString()}"
      yamlFile "$podTemplate"
    }
  }

  environment {
    NAME = "PriyankaLearnings"
    VERSION = "${env.BUILD_ID}"
    IMAGE_REPO = "sarthaksatish"
    GITHUB_TOKEN = credentials('githubpat')
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
            container(name: 'kaniko',shell:'/busybox/sh'){
              // sh "cp ${WORKSPACE}/Dockerfile ."
              sh "ls"
              withCredentials([file(credentialsId: 'docker-credentials', variable: 'DOCKER_CONFIG_JSON')]) {
                withEnv(['PATH+EXTRA=/busybox']) {
                  sh'''#!/busybox/sh
                  cp $DOCKER_CONFIG_JSON /kaniko/.docker/config.json
                  /kaniko/executor --force --dockerfile Dockerfile --context `pwd` --destination ${IMAGE_REPO}/${NAME}:${VERSION}
                  '''
                }
              }
              // kaniko.buildImage dockerfile: 'Dockerfile',
              // image: "${NAME}", tags: "${IMAGE_REPO}/${NAME}:${VERSION}"
              // sh "docker tag ${NAME}:latest ${IMAGE_REPO}/${NAME}:${VERSION}"
            }
          }
        }
      }

    stage('Clone/Pull Repo') {
      steps {
        script {
          if (fileExists('gitops-argocd')) {

            echo 'Cloned repo already exists - Pulling latest changes'

            dir("gitops-argocd") {
              sh 'git pull'
            }

          } else {
            echo 'Repo does not exists - Cloning the repo'
            sh 'git clone https://github.com/sarsatis/gitops-argocd'
          }
        }
      }
    }

    // stage('Update Manifest') {
    //   steps {
    //     dir("gitops-argocd/jenkins-demo") {

    //     }
    //   }
    // }

    stage('Commit & Push') {
      steps {
        script {
          dir("gitops-argocd/jenkins-demo") {
            withCredentials([usernamePassword(credentialsId: 'githubpat',
                  usernameVariable: 'username',
                  passwordVariable: 'password')]){
            encodedPassword = URLEncoder.encode("$password",'UTF-8')
            echo "sa ${encodedPassword}"
            sh "git config --global user.email 'jenkins@ci.com'"
            sh "git remote set-url origin https://${username}:${encodedPassword}@github.com/${username}/gitops-argocd.git"
            sh 'git checkout -b feature-test'
            sh 'git pull origin feature-test'
            sh 'sed -i "s#sarthaksatish.*#${IMAGE_REPO}/${NAME}:${VERSION}#g" deployment.yaml'
            sh 'cat deployment.yaml'
            sh 'git add -A'
            sh 'git commit -am "Updated image version for Build - $VERSION"'
            echo 'push started'
            sh "git push -u origin feature-test"
            }
            echo 'push complete'
          }
        }
      }
    }

    stage('Raise PR') {
      steps {
         script {
            withCredentials([usernamePassword(credentialsId: 'githubpat',
                  usernameVariable: 'username',
                  passwordVariable: 'password')]){
                encodedPassword = URLEncoder.encode("$password",'UTF-8')
                echo 'In Pr'

                sh"""
                curl -L \
                  -X POST \
                  -H "Accept: application/vnd.github+json" \
                  -H "Authorization: Bearer ${encodedPassword}"\
                  -H "X-GitHub-Api-Version: 2022-11-28" \
                  'https://api.github.com/repos/sarsatis/gitops-argocd/pulls' \
                  -d '{
                  "assignee": "sarsatis",
                  "assignees": [
                    "sarsatis"
                  ],
                  "base": "main",
                  "body": "Updated deployment specification with a new image version.",
                  "head": "feature-test",
                  "title": "Updated Solar System Image"
                }'

            """
                  }
            // sh "bash pr.sh"
        }
      }
    }
  }
}