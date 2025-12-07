# Advanced Chaos Garden Example

# AWS Provider
provider "aws" {
  alias  = "us-west"
  region = "us-west-2"
}

# GCP Provider
provider "google" {
  alias   = "us-central"
  project = "my-project"
  region  = "us-central1"
}

# Chaos Garden for AWS resources
module "chaos_garden_aws" {
  source = "../.."
  
  providers = {
    aws = aws.us-west
  }
  
  chaos_level = 5
  enabled     = true
  
  protected_resources = [
    "aws-production-rds",
    "aws-auth-lambda",
    "aws-s3-critical"
  ]
  
  chaos_schedule = "0 1 * * *"
  
  resource_tags = {
    Environment = "production"
    Cloud       = "AWS"
    Team        = "Platform"
  }
}

# Chaos Garden for GCP resources
module "chaos_garden_gcp" {
  source = "../.."
  
  providers = {
    google = google.us-central
  }
  
  chaos_level = 4
  enabled     = true
  
  protected_resources = [
    "gcp-production-sql",
    "gcp-cloud-run-auth",
    "gcp-storage-critical"
  ]
  
  chaos_schedule = "0 3 * * *"
  
  resource_tags = {
    Environment = "production"
    Cloud       = "GCP"
    Team        = "Platform"
  }
}

# High-risk chaos garden (use with extreme caution)
module "chaos_garden_high_risk" {
  source = "../.."
  
  chaos_level = 8
  enabled     = false  # Disabled by default for safety
  
  protected_resources = [
    "everything-critical"
  ]
  
  chaos_schedule = "0 4 * * 1"  # Only on Mondays at 4 AM
  
  resource_tags = {
    Environment = "experimental"
    Risk        = "high"
    Team        = "chaos-engineering"
  }
}

# Aggregate outputs
output "aws_chaos_summary" {
  value = module.chaos_garden_aws.chaos_summary
}

output "gcp_chaos_summary" {
  value = module.chaos_garden_gcp.chaos_summary
}

output "high_risk_chaos_summary" {
  value = module.chaos_garden_high_risk.chaos_summary
}

output "all_chaos_warnings" {
  value = concat(
    module.chaos_garden_aws.warnings,
    module.chaos_garden_gcp.warnings,
    module.chaos_garden_high_risk.warnings
  )
}
