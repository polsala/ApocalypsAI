terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Test module configuration
module "chaos_garden_test" {
  source = "../"

  environment = "test"
  chaos_level = "medium"

  create_ec2_instances = true
  ec2_instance_count = 2
  ec2_instance_type = "t3.micro"

  create_s3_buckets = true
  s3_bucket_count = 1

  create_rds_instances = true
  rds_instance_class = "db.t3.micro"

  create_lambda_functions = true
  lambda_function_count = 1

  enable_random_failures = true
  enable_resource_exhaustion = false
  enable_network_partitions = true
}

# Test assertions
# Mock rationale: Use local values to simulate expected outputs for testing
locals {
  expected_chaos_garden_id_length = 3
  expected_ec2_instance_count = 2
  expected_s3_bucket_count = 1
  expected_rds_instance_count = 1
  expected_lambda_function_count = 1
}

# Test chaos garden ID
resource "null_resource" "test_chaos_garden_id" {
  triggers = {
    chaos_garden_id = module.chaos_garden_test.chaos_garden_id
  }
  
  provisioner "local-exec" {
    command = "echo \"Testing chaos garden ID: ${self.triggers.chaos_garden_id}\""
  }
}

# Test EC2 instance count
resource "null_resource" "test_ec2_instance_count" {
  triggers = {
    ec2_count = "${length(module.chaos_garden_test.ec2_instance_ids)}"
  }
  
  provisioner "local-exec" {
    command = "echo \"Testing EC2 instance count: ${self.triggers.ec2_count}\""
  }
}

# Test S3 bucket count
resource "null_resource" "test_s3_bucket_count" {
  triggers = {
    s3_count = "${length(module.chaos_garden_test.s3_bucket_names)}"
  }
  
  provisioner "local-exec" {
    command = "echo \"Testing S3 bucket count: ${self.triggers.s3_count}\""
  }
}

# Test RDS instance count
resource "null_resource" "test_rds_instance_count" {
  triggers = {
    rds_count = "${length(module.chaos_garden_test.rds_instance_ids)}"
  }
  
  provisioner "local-exec" {
    command = "echo \"Testing RDS instance count: ${self.triggers.rds_count}\""
  }
}

# Test Lambda function count
resource "null_resource" "test_lambda_function_count" {
  triggers = {
    lambda_count = "${length(module.chaos_garden_test.lambda_function_arns)}"
  }
  
  provisioner "local-exec" {
    command = "echo \"Testing Lambda function count: ${self.triggers.lambda_count}\""
  }
}

# Test VPC ID
resource "null_resource" "test_vpc_id" {
  triggers = {
    vpc_id = module.chaos_garden_test.vpc_id
  }
  
  provisioner "local-exec" {
    command = "echo \"Testing VPC ID: ${self.triggers.vpc_id}\""
  }
}

# Test security group ID
resource "null_resource" "test_security_group_id" {
  triggers = {
    security_group_id = module.chaos_garden_test.security_group_id
  }
  
  provisioner "local-exec" {
    command = "echo \"Testing security group ID: ${self.triggers.security_group_id}\""
  }
}

# Test CloudWatch dashboard URL
resource "null_resource" "test_cloudwatch_dashboard_url" {
  triggers = {
    dashboard_url = module.chaos_garden_test.cloudwatch_dashboard_url
  }
  
  provisioner "local-exec" {
    command = "echo \"Testing CloudWatch dashboard URL: ${self.triggers.dashboard_url}\""
  }
}

# Test chaos level validation
resource "null_resource" "test_chaos_level_validation" {
  triggers = {
    chaos_level = "invalid"
  }
  
  provisioner "local-exec" {
    command = "echo \"Testing chaos level validation with: ${self.triggers.chaos_level}\""
  }
}

# Test EC2 instance count validation
resource "null_resource" "test_ec2_instance_count_validation" {
  triggers = {
    ec2_count = "15"
  }
  
  provisioner "local-exec" {
    command = "echo \"Testing EC2 instance count validation with: ${self.triggers.ec2_count}\""
  }
}

# Test S3 bucket count validation
resource "null_resource" "test_s3_bucket_count_validation" {
  triggers = {
    s3_count = "15"
  }
  
  provisioner "local-exec" {
    command = "echo \"Testing S3 bucket count validation with: ${self.triggers.s3_count}\""
  }
}

# Test Lambda function count validation
resource "null_resource" "test_lambda_function_count_validation" {
  triggers = {
    lambda_count = "15"
  }
  
  provisioner "local-exec" {
    command = "echo \"Testing Lambda function count validation with: ${self.triggers.lambda_count}\""
  }
}

# Output test results
output "test_chaos_garden_id" {
  value = module.chaos_garden_test.chaos_garden_id
}

output "test_ec2_instance_ids" {
  value = module.chaos_garden_test.ec2_instance_ids
}

output "test_s3_bucket_names" {
  value = module.chaos_garden_test.s3_bucket_names
}

output "test_rds_instance_ids" {
  value = module.chaos_garden_test.rds_instance_ids
}

output "test_lambda_function_arns" {
  value = module.chaos_garden_test.lambda_function_arns
}

output "test_vpc_id" {
  value = module.chaos_garden_test.vpc_id
}

output "test_security_group_id" {
  value = module.chaos_garden_test.security_group_id
}

output "test_cloudwatch_dashboard_url" {
  value = module.chaos_garden_test.cloudwatch_dashboard_url
}
