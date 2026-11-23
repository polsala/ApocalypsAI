provider "aws" {
  region = var.region
  # Mock rationale: No actual AWS credentials needed for terraform validate and plan.
  # The provider block is required for syntax, but no API calls are made during these test phases.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

variable "bucket_name_prefix" {}
variable "region" {}
variable "enable_replication" {}
variable "replication_destination_bucket_arn" {}
variable "enable_glacier_archive" {}
variable "glacier_transition_days" {}

module "apocalypse_vault" {
  source = "./modules/apocalypse-vault"

  bucket_name_prefix = var.bucket_name_prefix
  region             = var.region

  enable_replication             = var.enable_replication
  replication_destination_bucket_arn = var.replication_destination_bucket_arn

  enable_glacier_archive  = var.enable_glacier_archive
  glacier_transition_days = var.glacier_transition_days
}
