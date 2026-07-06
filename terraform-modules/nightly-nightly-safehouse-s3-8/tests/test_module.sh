#!/usr/bin/env bash
set -e
# Mock rationale: Ensure Terraform files contain required resources without invoking AWS.
# Verify that main.tf defines the expected AWS S3 resources.

grep -q 'resource "aws_s3_bucket"' src/main.tf

grep -q 'resource "aws_s3_bucket_versioning"' src/main.tf

grep -q 'resource "aws_s3_bucket_server_side_encryption_configuration"' src/main.tf

grep -q 'resource "aws_s3_bucket_lifecycle_configuration"' src/main.tf

grep -q 'resource "aws_s3_bucket_object"' src/main.tf

echo "All required resources are present."
