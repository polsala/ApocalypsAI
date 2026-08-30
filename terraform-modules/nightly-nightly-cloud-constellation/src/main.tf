terraform {
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

provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "celestial_bucket" {
  bucket = "${var.bucket_name_prefix}-${lower(replace(var.constellation_name, " ", "-"))}-${random_id.suffix.hex}"
  acl    = "private" # Best practice: private by default

  tags = {
    Name                = "${var.bucket_name_prefix}-${var.constellation_name}"
    Constellation       = var.constellation_name
    CelestialCoordinates = var.celestial_coordinates
    ManagedBy           = "ApocalypsAI-NightlyIntegrator"
  }

  # Enable versioning for data integrity
  versioning {
    enabled = true
  }

  # Server-side encryption by default
  server_side_encryption configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  # Block public access for security
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "random_id" "suffix" {
  byte_length = 4
}
