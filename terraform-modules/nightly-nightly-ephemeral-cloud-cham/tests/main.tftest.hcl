# Mock rationale: To ensure deterministic and offline testing for a Terraform module
# that typically interacts with cloud providers, we employ several strategies:
# 1.  `command = "plan"`: The test only performs a `terraform plan`, avoiding actual
#     resource creation or modification in the cloud. This makes the test non-destructive
#     and faster.
# 2.  Mocking `ami_id`: The `ami_id` variable is explicitly set to a dummy value
#     ("ami-0abcdef1234567890") in the test configuration. This prevents Terraform
#     from attempting to fetch the latest AMI from AWS using `data "aws_ami"`,
#     which would require AWS credentials and network access, thus making the test
#     more "offline".
# 3.  Assertions on `plan.resource_changes`: We assert that specific resources
#     are *planned* for creation. This validates the module's logic and resource
#     definitions without needing to interact with the live AWS API beyond provider
#     initialization (which still requires network access to download provider binaries,
#     a common limitation for "offline" Terraform testing without pre-downloaded plugins).
#     Truly 100% offline Terraform testing often involves complex provider mocking
#     frameworks or pre-seeding the Terraform cache. For this utility, this approach
#     provides a good balance of determinism, speed, and reduced external dependencies.

run "plan_and_validate_resources" {
  command = "plan"

  variables {
    aws_region = "us-east-1"
    instance_type = "t2.micro"
    bucket_name_prefix = "test-ephemeral"
    ami_id = "ami-0abcdef1234567890" # Mock rationale: Hardcode AMI to avoid data lookup and network call.
  }

  assert {
    condition     = plan.resource_changes["aws_vpc.main"].change.actions == ["create"]
    error_message = "VPC should be planned for creation."
  }

  assert {
    condition     = plan.resource_changes["aws_subnet.main"].change.actions == ["create"]
    error_message = "Subnet should be planned for creation."
  }

  assert {
    condition     = plan.resource_changes["aws_internet_gateway.main"].change.actions == ["create"]
    error_message = "Internet Gateway should be planned for creation."
  }

  assert {
    condition     = plan.resource_changes["aws_route_table.main"].change.actions == ["create"]
    error_message = "Route Table should be planned for creation."
  }

  assert {
    condition     = plan.resource_changes["aws_route_table_association.main"].change.actions == ["create"]
    error_message = "Route Table Association should be planned for creation."
  }

  assert {
    condition     = plan.resource_changes["aws_security_group.instance_sg"].change.actions == ["create"]
    error_message = "Security group should be planned for creation."
  }

  assert {
    condition     = plan.resource_changes["aws_instance.ephemeral_server"].change.actions == ["create"]
    error_message = "EC2 instance should be planned for creation."
  }

  assert {
    condition     = plan.resource_changes["aws_s3_bucket.ephemeral_storage"].change.actions == ["create"]
    error_message = "S3 bucket should be planned for creation."
  }

  assert {
    condition     = plan.resource_changes["random_id.bucket_suffix"].change.actions == ["create"]
    error_message = "Random ID for bucket suffix should be planned for creation."
  }
}
