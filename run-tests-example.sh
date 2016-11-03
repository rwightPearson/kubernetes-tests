#!/bin/bash

#THis is an example script that may be placed on the Master node of a kubernetes cluster (user data) to execute containerized tests at start-up.
#Our team deploys our kubernetes PaaS from TravisCI using terrraform. Once deployed, travicCI accesses this script on the master and executes it to test the PaaS

GIT_REPO=git@github.com:pearsontechnology/kubernetes-tests.git

evaluateExitCode(){
  if [ "$?" != "0" ]; then
     cd && rm -rf $tmp
     exit 1
  fi
}

sudo chmod 600 /root/.ssh/bitesize.key
sudo chmod 600 /root/.ssh/git.key
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/git.key
ssh-keyscan github.com >> ~/.ssh/known_hosts

tmp=${TMPDIR-/tmp}
        tmp=$tmp/run-containerized-tests.$RANDOM.$$
        (umask 077 && mkdir $tmp) || {
                echo "Could not create temporary directory! Exiting." 1>&2
                exit 1
        }

echo -e "Host github.com\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config && chmod 600 ~/.ssh/config
echo "Cloning Branch=$TEST_BRANCH of $GIT_REPO"
cd $tmp && git clone -q -b $TEST_BRANCH $GIT_REPO


evaluateExitCode

kubectl get namespace test-runner > /dev/null 2>&1 || kubectl create namespace test-runner


#The kubernetes-tests container requires secrets to be set to enable ssh'ing to other nodes in the cluster as well as to clone the kubernetes-tests repository.
# Below is an overview of these secrets:
   # bitesize.key :  THis is the key used to ssh from yor master kubernetes node to other nodes in the private subnet
   # kubectl-client-key : This is the client key used by kubectl which will be used in the container to setup kubectl config
   # kubectl-ca : This is the certificate authority used by kubectl which will be used in the container to setup kubectl config
   # jenkins-user and jenkins-pass : The secrets are used by the jenkins-dep/svc/ing.yaml files to build a new test container image
   # git-username/password : Used by the container to access git and retrieve the kubernetes-tests repo for Execution

kubectl get secretes test-runner-secrets --namespace=test-runner > /dev/null 2>&1 || kubectl create secret generic test-runner-secrets \
  --from-file=bitesize-priv-key=/root/.ssh/bitesize.key \
  --from-file=kubectl-client-key=/root/.ssh/bitesizessl.pem \
  --from-file=kubectl-ca=/root/.ssh/ca.pem \
  --from-file=git-key=/root/.ssh/git.key \
  --from-literal=jenkins-user=jenkins-user \
  --from-literal=jenkins-pass=jenkins-pass \
  --from-literal=git-username=username \
  --from-literal=git-password=git-token \
  --namespace=test-runner

cd kubernetes-tests

#Run all tests and fail after 10 minutes (600s) if test job does not succeed.
#Need to be cognizant of the -e field with travis CI. Travis CI builds will die after 10 minutes with no response
./run-containerized-tests.sh -t all -b $TEST_BRANCH -e 600
evaluateExitCode

cd && rm -rf $tmp
