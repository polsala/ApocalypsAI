# Tests for Nightly Terraform Void Garden

This directory contains tests for the Terraform module.

## Running Tests

1. Ensure you have the AWS CLI configured with appropriate permissions.
2. Run `terraform init` in this directory.
3. Run `terraform plan` to see what will be created.
4. Run `terraform apply` to create the resources.
5. Verify the outputs.
6. Run `terraform destroy` to clean up.

## Test Plan

- [x] Verify that the garden URL is not empty.
- [x] Verify that the easter egg path is correct.
- [x] Verify that the resources are created with the correct tags.
- [x] Verify that the auto scaling group has the correct min, max, and desired capacity.
- [x] Verify that the security group allows HTTP and SSH access.
- [x] Verify that the CloudWatch alarm is created and points to the SNS topic.
