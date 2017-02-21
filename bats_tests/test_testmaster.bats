#!/usr/bin/env bats

set -o pipefail

# Services

@test "Verify that all test services are running successfully" {
    curl -s -o /dev/null -w "%{http_code}" test-master.default.svc.cluster.local/services | grep 200
}
