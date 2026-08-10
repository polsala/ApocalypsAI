terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

variable "bucket_name_prefix" {
  description = "Prefix for the S3 bucket name"
  type        = string
  default     = "apocalypse-supply"
}

# Generate a random suffix to ensure global uniqueness
resource "random_pet" "suffix" {
  length = 2
}

resource "aws_s3_bucket" "supply_bucket" {
  bucket        = "${var.bucket_name_prefix}-${random_pet.suffix.id}"
  force_destroy = true

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  lifecycle_rule {
    id      = "expire-old-supplies"
    enabled = true

    expiration {
      days = 30
    }

    filter {}
  }

  tags = {
    Purpose = "ApocalypseSupply"
  }
}

resource "aws_s3_bucket_object" "supply_list" {
  bucket                 = aws_s3_bucket.supply_bucket.id
  key                    = "supply-list.txt"
  content = <<-EOT
    - Water (2 liters per person per day)
    - Non-perishable food
    - First aid kit
    - Flashlight + batteries
    - Multi-tool
    - Radio (hand crank)
  EOT
  server_side_encryption = "AES256"
}
