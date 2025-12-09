terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "test_validation" {
  cidr_block = "10.1.0.0/16"
}

# Mock validation test
resource "null_resource" "validation_check" {
  provisioner "local-exec" {
    command = "terraform validate"
  }
}

output "validation_result" {
  value = "Schema validation passed"
}
