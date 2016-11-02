#!/usr/bin/env bats

set -o pipefail

load helpers

# Infrastructure

@test "master" {
  kubectl get node master-$STACK_ID.$ENVIRONMENT.kube
}

@test "minion" {
  kubectl get nodes --no-headers | grep minion
}

@test "loadbalancer" {
  kubectl get nodes --no-headers | grep loadbalancer
}
