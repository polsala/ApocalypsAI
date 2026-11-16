#!/bin/sh
# Mock rationale: We cannot deterministically control the actual system time or external NTP server
# responses in a CI/CD environment. Mocking `ntpdate` ensures the test verifies the `stabilize.sh`
# script's logic (calling `ntpdate` and handling its exit code) without relying on external network
# access or privileged time-setting operations. This makes the test fast, reliable, and offline.

echo "MOCK: ntpdate called with $*"
# Simulate success for testing purposes
exit 0
