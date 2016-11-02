#!/usr/bin/python
import boto3
import os

##Verify both front-end live and pre-live loadbalancers are running
def test_prelive_and_live_loadbalancers_exist():
    elb = boto3.client('elb', region_name=os.environ["REGION"])
    env = os.environ["ENVIRONMENT"]
    frontendprelive = "frontend-" + env + "-prelive"
    frontendlive = "frontend-" + env + "-live"
    bals=elb.describe_load_balancers()
    lbcount=0
    for elb in bals['LoadBalancerDescriptions']:
        if (elb['LoadBalancerName'] == frontendprelive): lbcount += 1
        if (elb['LoadBalancerName'] == frontendlive): lbcount += 1

    assert lbcount ==  2  #Should be two load balancers returned
