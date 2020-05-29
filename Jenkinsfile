pipeline {
  agent {
    node {
      label 'master'
    }

  }
  stages {
    stage('build') {
      steps {
        git(url: 'git@github.com:S594805915/jenkinsci.git', branch: 'master')
      }
    }

  }
}