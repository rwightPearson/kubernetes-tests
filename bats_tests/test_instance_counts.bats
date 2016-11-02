#!/usr/bin/env bats

set -o pipefail

load helpers

# Infrastructure

@test "minion count" {
  MINIONS=`kubectl get nodes --selector=role=minion --no-headers | wc -l`
  min_value_met $MINION_COUNT $MINIONS
}

@test "loadbalancer count" {
  LOADBALANCERS=`kubectl get nodes --selector=role=loadbalancer --no-headers | wc -l`
  values_equal $LOADBALANCERS $LOADBALANCERS
}
