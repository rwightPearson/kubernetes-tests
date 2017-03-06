#!/usr/bin/env bats

set -o pipefail

# Services
# Temporarily modified to only check for test-tpr-s3.
@test "Verify that all test services are running successfully" {
    curl -s -o /dev/null -w "%{http_code}" test-master.default.svc.cluster.local/services | grep 200
}
