terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  # Use localstack for testing
  alias = "localstack"
  
  endpoints {
    s3              = "http://localhost:4566"
    dynamodb        = "http://localhost:4566"
    lambda          = "http://localhost:4566"
    cloudwatch      = "http://localhost:4566"
    iam             = "http://localhost:4566"
  }
}

module "chaos_garden_test" {
  source = "../"
  
  providers = {
    aws = aws.localstack
  }
  
  garden_name    = "test-chaos-garden"
  chaos_factor   = 0.5  # 50% chance for testing
  s3_buckets     = ["test-flower", "test-tree"]
  dynamodb_tables = ["test-insect", "test-bird"]
  lambda_functions = ["test-watering"]
}

# Test assertions
resource "null_resource" "test_assertions" {
  triggers = {
    garden_name = module.chaos_garden_test.garden_health
  }
  
  provisioner "local-exec" {
    command = "echo 'Test: Garden health is ${self.triggers.garden_name}'"
  }
}

# Mock AWS resources for testing
resource "aws_s3_bucket" "mock_bucket" {
  provider = aws.localstack
  bucket   = "mock-test-bucket"
  acl      = "private"
  
  # Mock rationale: Simulate AWS S3 bucket for testing without real AWS resources
}

resource "aws_dynamodb_table" "mock_table" {
  provider     = aws.localstack
  name         = "mock-test-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
  
  attribute {
    name = "id"
    type = "S"
  }
  
  # Mock rationale: Simulate AWS DynamoDB table for testing without real AWS resources
}

# Test plan
resource "null_resource" "test_plan" {
  provisioner "local-exec" {
    command = <<EOT
      echo "=== Chaos Garden Test Plan ==="
      echo "1. Verify S3 buckets are created"
      echo "2. Verify DynamoDB tables are created"
      echo "3. Verify Lambda functions are created"
      echo "4. Verify chaos destruction mechanism works"
      echo "5. Verify CloudWatch dashboard is created"
      echo "6. Verify outputs are correct"
      echo "=== End Test Plan ==="
    EOT
  }
}
