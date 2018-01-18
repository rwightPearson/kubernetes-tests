# kubernetes-tests

Kubernetes (k8s) containerized/deployable test suite.  This repo allows the execution of BATS, INSPEC, and Python tests against a deployed PaaS.  Through the usage of kubernetes jobs a test contianer spins up execute a specified number of tests against the nodes within the kubernetes PaaS.  

==========================================================================================
**Getting Started** 

1) Get access to a test container docker image, which is vital to being able to run the containerized test suite. The latest version is hosted on pearson's docker hub registry (docker pull pearsontechnology/test-executor-app).  The test container (test-executor-app) is built from this repo, using a custom Pearson jenkins plugin that is not yet open sourced. So, pull from docker hub and add it as the image location in [job.yaml](./job.yaml) and [job-withargs.yaml](./job-withargs.yaml) instead of the bitesize-registry location that is currently baselined in those files.

2) Familiarize yourself with some of the files that are used to start the kubernetes jobs:

- [run-tests-example.sh](./run-tests-example.sh) - Sets up environment on kubernetes master node and calls the run-containerized-tests.sh script. This script should be placed on your kubernetes master node.
- [run-containerized-tests.sh](./run-containerized-tests.sh) - This file configures the kubernetes job via avaialble options,  runs the job, monitors progress, and then reports results from completed or error pod logs that were part of the job.
- [run.sh](./test-executor-app/run.sh) - This is the test container Docker entry point. It builds up a hosts.yaml file for a list of hosts that will be under tests in the cluster, configures kubectl, and then starts the tests by launching testRunner.py
- [testRunner.py](./test-executor-app/testRunnery.py) - This file is built into the test container image and is responsible for execution of the INSPEC/BATS/Python tests in the kubernetes-tests repo.

3) Review what is required in your Kubernetes PaaS environment to run tests. This is detailed in the section titled [**What's Required By the Test Container to Run?**](#RunTests)

==========================================================================================

The Pearson team utilizes kubernetes-tests to execute tests against the PaaS. On our deployment, we use a startup script (run-tests.sh) to kick off the containerized tests from our CI/CD pipeline (TravisCI). You may review the [run-tests-example.sh](./run-tests-example.sh) included in this repo, which is an example of our run-tests.sh script that may be used on the master node of your kubernetes cluster to kick off tests for each deployed PaaS. This is how we utilize it:

**Run All Tests From a Specific kubernetes-tests Branch Against a PaaS Deployment:**

```
1) ssh centos@master
2) sudo su -;
3) export TEST_BRANCH=${kubernetes-tests Branch}
3) cd /tmp/test/kubernetes
4) ./run-tests.sh ${TEST_BRANCH}  
```

**View Test Results for a Bitesize PaaS Deployment:**

```
1) ssh centos@master
2) sudo su -;
3) cat /root/kubernetes-containerized-tests.log
```

==========================================================================================
<a id="Environment"></a>

**What's Required By the Test Container to Run?**

First off, the test container requires secrets to be set to enable ssh'ing into other nodes in the cluster as well as to interact with Git. Below is an overview of these secrets and how to set them:

- **bitesize.key** :  This is the key used to ssh from yor master kubernetes node to other nodes in the private subnet
- **kubectl-client-key** : This is the client key used by kubectl which will be used in the container to setup kubectl config
- **kubectl-ca** : This is the certificate authority used by kubectl which will be used in the container to setup kubectl config
- **jenkins-user and jenkins-pass** : These username/passwords are used by the [jenkins-dep.yaml](./test-executor-app/jenkins-dep.yaml), [jenkins-svc.yaml](./test-executor-app/jenkins-svc.yaml), [jenkins-ing.yaml](./test-executor-app/jenkins-ing.yaml)  files to build a new test container image. The jenkins image and jenkins plugin are not yet opensourced.
- **git-username/password** : Used by the container to access git and retrieve the kubernetes-tests repo for Execution. This is your git username and git access token.

```
kubectl get secrets test-runner-secrets --namespace=test-runner > /dev/null 2>&1 || kubectl create secret generic test-runner-secrets \
  --from-file=bitesize-priv-key=/root/.ssh/bitesize.key \
  --from-file=kubectl-client-key=/root/.ssh/bitesizessl.pem \
  --from-file=kubectl-ca=/root/.ssh/ca.pem \
  --from-file=git-key=/root/.ssh/git.key \
  --from-literal=jenkins-user=jenkins-user \
  --from-literal=jenkins-pass=jenkins-pass \
  --from-literal=git-username=username \
  --from-literal=git-password=git-token \
  --namespace=test-runner
```

Once secrets are set, you also need some environment variables. The varibales are passed along to the test container through the kubernetes job via the [job.yaml](./job.yaml) or [job-withargs.yaml](./job-withargs.yaml) files.  Below is an overview of these environment variables, which are utilized by the test container at its docker point of entry to retrieve instances to test as well as to setup kubectl within the test container. Usage may be reviewed in [run.sh](./test-executor-app/run.sh) and [testRunney.py](./test-executor-app/testRunnery.py). These environment variables are set on our kubernetes master node as the root user.

```
export REGION=us-west-2 #Deployed region for the PaaS
export STACK_ID=a       #Which stack a/b is under test
export ENVIRONMENT=ben  #environment name
export TEST_BRANCH=dev  #kubernetes-tests branch you are testing with
export MINION_COUNT=2   #From bitsize deployment terraform.tfvars
export KUBE_PASS=${pass}#From bitesize deployment terraform.tfvars
```
==========================================================================================

**Test Execution Options/Examples:**

Example1: Execute all tests (python/inspec/bats within kubernetes-tests) against your deployment

```
     ./run-containerized-tests.sh -t all
```
Example1: Execute all tests (python/inspec/bats within kubernetes-tests) aginst your deployment from a specific kubernetes-tests branch

```
     ./run-containerized-tests.sh -t all -b mybranch
```

Example2: Execute a bats test 100 times against your deployment using at most 5 pods in parrallel to reach the 100 desired completions

```
     ./run-containerized-tests.sh -t bats -f test_namespace_isolation.bats -c 100 -p 5
```

Example3: Execute a python test against your deployment

```
     ./run-containerized-tests.sh -t python -f test_namespace_isolation
```

     Note:  When specifying python tests, you omit the .py extension from your filename

Example4: Execute two inspec tests against your deployment

      Ensure your tests are listed under the instance type that they should be executed  against in <kubernetes-tests>/inspec_tests/config.yaml

```
     ./run-containerized-tests.sh -t inspec -f master_spec.rb -f minion_spec.rb
```


**Available Options: run-containerized-tests.sh**

Execute  ./run-containerized-tests.sh  without any arguments to get command help

```
Overall Usage: ./run-containerized-tests.sh -t <all|python|bats|inspec> -p <# pods> -c <# completions> -b <branch> -e <timeout> -f <file1> -f <file2> -f <filen>
```
==========================================================================================

 **Making Source Code updates to the test-executor-app  (<kubernetes-tests>/test-executor-app) will require a new docker image version to be built**

Deployment of jenkins to build the testcontainer image requires the open sourcing (TBD) of our Jenkins Plugin: [Pearson Jenkins Plugin](https://github.com/pearsontechnology/deployment-pipeline-jenkins-plugin)

 1.  First deploy your Jenkins Instance on Master
   ```
      kubectl create namespace test-runner
      kubectl create -f jenkins-dep.yaml
      kubectl create -f jenkins-svc.yaml
      kubectl create -f jenkins-ing.yaml
   ```

 2. Add your frontend ELB Public IP as jenkins.test-runner.prsn-dev.io to your hosts file
 3. Navigate to jenkins.test-runner.prsn-dev.io with the credentials specified in jenkins-dep.yaml for login
 4. Commit your code changes to the kubernetes-tests repo which will start new jobs in your jenkins deployment.
 5. Once all jobs complete (environments is expected to fail as we are not deploying), update **job.yaml** and **job-withargs.yaml**    to include the new test container image version for the test-executor-app docker image version produced and found in the  test-executor-app-docker-image job in your jenkins deployment

==========================================================================================

**kubernetes-tests/inspec_tests/config.yaml**

This file is utilized by the test container within the [testRunnery.py](./test-executor-app/testRunnery.py) script to determine what INSPEC tests to run. Specifies  the server types and the associated INSPEC controls that should be executed against the given server type.  The test container job will evaluate this config file against the available server name tags in your deployment and will apply those control tests against your server.  Executing ./run-containerized-tests.sh -t all" with the config below in place would execute the two control tests against master and bastion instances in your deployment.  More information on how to write Chef Inspec tests may be found [here](https://docs.chef.io/inspec.html)

```
    master:
      - test_master_spec.rb
    etcd:
    nfs:
    loadbalancer:
    stackstorm:
    auth:
    minion:
    bastion:
      - test_bastion_spec.rb
```
