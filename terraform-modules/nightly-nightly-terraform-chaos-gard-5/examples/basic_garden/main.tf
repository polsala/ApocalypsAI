terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

module "chaos_garden" {
  source = "../../"
  
  garden_name = "apocalypsi-chaos-garden"
  
  # Resource configuration
  create_ec2_instances = true
  ec2_instance_count  = 2
  
  create_lambda_functions = true
  lambda_function_count  = 1
  
  create_s3_buckets = true
  s3_bucket_count  = 1
  
  create_rds_instances = false
  rds_instance_count  = 0
  
  # Chaos configuration
  enable_chaos_experiments = true
  chaos_schedule          = "cron(0 */2 * * ? *)" # Every 2 hours
  
  # Cleanup configuration
  enable_automatic_cleanup = true
  cleanup_schedule         = "cron(0 2 * * ? *)" # Daily at 2 AM
  
  # Monitoring
  enable_cloudwatch_dashboard = true
  enable_alarms              = true
  
  # Optional: SNS topic for alarms
  # sns_topic_arn = "arn:aws:sns:us-east-1:123456789012:chaos-alarms"
}
