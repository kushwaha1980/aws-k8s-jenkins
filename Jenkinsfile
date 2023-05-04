pipeline {
    agent {
        kubernetes {
            defaultContainer "docker-python"
            yaml """
            apiVersion: v1
            kind: pod
            metadata:
                annotations:
                    iam.amazonaws.com/role: "${JENKINS_SLAVE_IAM_ROLE}"
            spec:
                containers:
                - name: teraform12
                  image: hashicorp/terraform:1.2.8
                  command:
                  - cat
                  tty: true
                - name: docker-python
                  image: python:3.8
                  command:
                  - cat
                  ttye: true
                  volumeMounts:
                    - name: shared-build-output
                      mountPath: /var/run/outputs
                    - name: shared-m2
                      mountPath: /var/run/shared-m2
                    - name: container-storage
                      mountPath: /var/lib/containers
                  volumes:
                    - name: shared-m2
                      emptyDir: {}
                    - name: shared-build-output
                      emptyDir: {}
                    - name: container-storage
                      emptyDir: {}
            """
        }
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        parallelsAlwaysFailFast()
        ansiColor('xterm')
    }

    stages {
        stage {
            container('docker-python') {
                script {
                    sh '''
                    python3 -m pip install --upgrade awscli
                    sh scripts/build_artifacts.sh && echo "build successfull !!" || error "build failed!!"
                    '''
                }
            }
        }
    }
}