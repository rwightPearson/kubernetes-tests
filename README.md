# kubernetes-tests

Repository for PaaS containerized/deployable test suite.  This repo allows the execution of BATS, INSPEC, and Python tests (tests must be resident in the repo kubernetes-tests/bats_tests, kubernetes-tests/python_tests, or kubernetes-tests/inspec_tests/controls) against a deployed Bitesize PaaS.  Through the usage of kubernetes jobs, it spins up a test container that executes a specified number of tests against the PaaS.

==========================================================================================

Bitesize PaaS deployments include a "run-tests.sh" script that is used to start up containerized tests for each deployment.   Below are the ways this script is utilized within a Bitesize deployment.

**Run All Tests Set Against Bitesize PaaS Deployment:**

```
1) ssh centos@master
2) sudo su -;
3) cd /tmp/test/kubernetes
4) ./run-tests.sh    
```

**View Test Results for a Bitesize PaaS Deployment:**

```
1) ssh centos@master
2) sudo su -;
3) cat /root/kubernetes-containerized-tests.log
```

**Run All Tests From a Specific kubernetes-tests Branch Against a Bitesize PaaS Deployment:**

```
1) ssh centos@master
2) sudo su -;
3) export TEST_BRANCH=${kubernetes-tests Branch}
3) cd /tmp/test/kubernetes
4) ./run-tests.sh ${TEST_BRANCH}
```

==========================================================================================

Running tests against Bitesize from outside of a deployment (directly from kubernetes-tests repo) may also be performed.  Below is how that is accomplished:

**Run Containerized Tests Against Bitesize PaaS Deployment **

```
1) git clone git@github.com:pearsontechnology/kubernetes-tests.git
2) cd kubernetes-tests
3)Export environment variables the kubernetes job will need since we are not running on the master PaaS instance.
	export REGION=us-west-2  
	export STACK_ID=a
	export ENVIRONMENT=ben
	export TEST_BRANCH=dev  #kubernetes-tests branch you are testing with
	export MINION_COUNT=2   #From bitsize deployment terraform.tfvars
	export KUBE_PASS=${pass}#From bitesize deployment terraform.tfvars
4) Execute tests as defined in example section below.
```
==========================================================================================

**Test Execution Examples:**

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

 **Making Source Code updates to the test-executor-app  (changes made in <kubernetes-tests>/test-executor-app will require a new docker image version to be built)**

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
 5. Once all jobs complete (environments is expected to fail as we are not deploying), update test-job.yaml and test-job-withargs.yaml
    to include the new test container image version for the
    test-executor-app docker image version produced and found in the
    test-executor-app-docker-image job in your jenkins deployment

**kubernetes-tests/inspec_tests/config.yaml**

Specifies  the server types and the associated INSPEC controls that should be executed against the given server type.  The test container job will evaluate this config file against the available server name tags in your deployment and will apply those control tests against your server.  Executing ./run-containerized-tests.sh -t all" with the config below in place would execute the two control tests against master and bastion instances in your deployment.  More information on how to write Chef Inspec tests may be found [here](https://docs.chef.io/inspec.html)

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
