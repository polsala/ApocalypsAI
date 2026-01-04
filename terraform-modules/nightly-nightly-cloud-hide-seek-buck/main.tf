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
  region = "us-east-1" # Default region, can be overridden by TF_VAR_aws_region or provider block in root module
}

resource "aws_s3_bucket" "hide_and_seek_bucket" {
  bucket = var.bucket_name_prefix != "" ? "${var.bucket_name_prefix}-${random_string.suffix.result}" : "hide-seek-${random_string.suffix.result}"
  acl    = "private" # Keep it private by default

  tags = merge(var.common_tags, {
    "Game"        = "CloudHideAndSeek"
    "WhimsyLevel" = "High"
    "Ephemeral"   = "True"
    "CreatedBy"   = "ApocalypsAI"
  })
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}
