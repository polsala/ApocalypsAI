#!/usr/bin/env bash
# Mock rationale: offline test, just verify that Terraform files contain required resources.

set -e

if grep -q 'resource "aws_s3_bucket"' main.tf && grep -q 'resource "aws_iam_policy"' main.tf; then
  echo "All required resources present."
  exit 0
else
  echo "Missing required resources."
  exit 1
fi
