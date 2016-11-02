#!/usr/bin/python
import boto3
import os
import yaml
from subprocess import Popen, PIPE

def run_script(command):
    global failuresReceived
    process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    errorCode = process.returncode
    return stdout,stderr,errorCode

def test_no_ansible_playbook_failures_on_stackstorm_nodes():
    hostYaml="/var/hosts.yaml"
    with open(hostYaml, 'r') as ymlfile1:  # hosts to test
        contents = yaml.load(ymlfile1)
        for host in contents['hosts']:
            if ("stackstorm" in host['name']):
                # Verify the Ansible Playbook Finished and there is no failures.  Look for the ansible RECAP and find any instances of failed=x where x is greater than zero
                cmd="ssh -i ~/.ssh/bitesize.key root@{0} 'cat /var/log/cloud-init-output.log | grep -A 2 RECAP | grep -o 'failed=[1-9][0-9]*''".format(host['value'])
                stdout,stderr,errorCode=run_script(cmd)
                assert errorCode != 0   #If Error Code is non-zere, then no Playbook/RECAP failures were found in the log

def test_no_ansible_playbook_failures_on_authn_nodes():
    hostYaml="/var/hosts.yaml"
    with open(hostYaml, 'r') as ymlfile1:  # hosts to test
        contents = yaml.load(ymlfile1)
        for host in contents['hosts']:
            if ("authn" in host['name']):
                # Verify the Ansible Playbook Finished and there is no failures.  Look for the ansible RECAP and find any instances of failed=x where x is greater than zero
                cmd="ssh -i ~/.ssh/bitesize.key centos@{0} 'cat /var/log/cloud-init-output.log | grep -A 2 RECAP | grep -o 'failed=[1-9][0-9]*''".format(host['value'])
                stdout,stderr,errorCode=run_script(cmd)
                assert errorCode != 0   #If Error Code is non-zere, then no Playbook/RECAP failures were found in the log

def test_no_ansible_playbook_failures_on_loadbalancer_nodes():
    hostYaml="/var/hosts.yaml"
    with open(hostYaml, 'r') as ymlfile1:  # hosts to test
        contents = yaml.load(ymlfile1)
        for host in contents['hosts']:
            if ("loadbalancer" in host['name']):
                # Verify the Ansible Playbook Finished and there is no failures.  Look for the ansible RECAP and find any instances of failed=x where x is greater than zero
                cmd="ssh -i ~/.ssh/bitesize.key centos@{0} 'cat /var/log/cloud-init-output.log | grep -A 2 RECAP | grep -o 'failed=[1-9][0-9]*''".format(host['value'])
                stdout,stderr,errorCode=run_script(cmd)
                assert errorCode != 0   #If Error Code is non-zere, then no Playbook/RECAP failures were found in the log

def test_no_ansible_playbook_failures_on_nfs_nodes():
    hostYaml="/var/hosts.yaml"
    with open(hostYaml, 'r') as ymlfile1:  # hosts to test
        contents = yaml.load(ymlfile1)
        for host in contents['hosts']:
            if ("nfs" in host['name']):
                # Verify the Ansible Playbook Finished and there is no failures.  Look for the ansible RECAP and find any instances of failed=x where x is greater than zero
                cmd="ssh -i ~/.ssh/bitesize.key root@{0} 'cat /var/log/cloud-init-output.log | grep -A 2 RECAP | grep -o 'failed=[1-9][0-9]*''".format(host['value'])
                stdout,stderr,errorCode=run_script(cmd)
                assert errorCode != 0   #If Error Code is non-zere, then no Playbook/RECAP failures were found in the log

def test_no_ansible_playbook_failures_on_bastion_nodes():
    hostYaml="/var/hosts.yaml"
    with open(hostYaml, 'r') as ymlfile1:  # hosts to test
        contents = yaml.load(ymlfile1)
        for host in contents['hosts']:
            if ("bastion" in host['name']):
                # Verify the Ansible Playbook Finished and there is no failures.  Look for the ansible RECAP and find any instances of failed=x where x is greater than zero
                cmd="ssh -i ~/.ssh/bitesize.key root@{0} 'cat /var/log/cloud-init-output.log | grep -A 2 RECAP | grep -o 'failed=[1-9][0-9]*''".format(host['value'])
                stdout,stderr,errorCode=run_script(cmd)
                assert errorCode != 0   #If Error Code is non-zere, then no Playbook/RECAP failures were found in the log

def test_no_ansible_playbook_failures_on_minion_nodes():
    hostYaml="/var/hosts.yaml"
    with open(hostYaml, 'r') as ymlfile1:  # hosts to test
        contents = yaml.load(ymlfile1)
        for host in contents['hosts']:
            if ("minion" in host['name']):
                # Verify the Ansible Playbook Finished and there is no failures.  Look for the ansible RECAP and find any instances of failed=x where x is greater than zero
                cmd="ssh -i ~/.ssh/bitesize.key centos@{0} 'cat /var/log/cloud-init-output.log | grep -A 2 RECAP | grep -o 'failed=[1-9][0-9]*''".format(host['value'])
                stdout,stderr,errorCode=run_script(cmd)
                assert errorCode != 0   #If Error Code is non-zere, then no Playbook/RECAP failures were found in the log

def test_all_nodes_using_ansible_playbook_clone_the_ansible_branch():
    ansible_branch=os.environ["ANSIBLE_BRANCH"]
    hostYaml="/var/hosts.yaml"
    with open(hostYaml, 'r') as ymlfile1:  # hosts to test
        contents = yaml.load(ymlfile1)
        for host in contents['hosts']:
            if ("nfs" in host['name'] or "bastion" in host['name'] or "stackstorm" in host['name']):
                cmd = "echo \"Host {0}\n\tStrictHostKeyChecking no\n\" >> ~/.ssh/config".format(host['value'])
                run_script(cmd)
                cmd="ssh -i ~/.ssh/bitesize.key root@{0} 'cat /var/log/cloud-init-output.log | grep -o \"git clone .* git@github.com:pearsontechnology/ansible-roles.git aws\" | grep -o '{1}''".format(host['value'],ansible_branch)
                stdout,stderr,errorCode=run_script(cmd)
                assert errorCode == 0   #If error code is zero, then ANSIBLE_BRANCH was used to clone the ansible-roles repo
            elif ("authn" in host['name'] or "loadbalancer" in host['name'] or "minion" in host['name']):
                cmd = "echo \"Host {0}\n\tStrictHostKeyChecking no\n\" >> ~/.ssh/config".format(host['value'])
                run_script(cmd)
                cmd="ssh -i ~/.ssh/bitesize.key centos@{0} 'cat /var/log/cloud-init-output.log | grep -o \"git clone .* git@github.com:pearsontechnology/ansible-roles.git aws\" | grep -o '{1}''".format(host['value'],ansible_branch)
                stdout,stderr,errorCode=run_script(cmd)
                assert errorCode == 0   #If error code is zero, then ANSIBLE_BRANCH was used to clone the ansible-roles repo
