# Example: Production-Safe Chaos Monkey Configuration

# In production, we typically don't enable chaos monkey
# But this shows how you might configure it safely

module "chaos_monkey" {
  source = "../.."
  
  # NEVER enable in production without extreme caution
  enabled = false
  
  # Conservative settings for when chaos is enabled
  destruction_probability = 0.01  # 1% chance
  max_destructions_per_run = 1
  
  # Only target non-critical resources
  target_resources = [
    "aws_instance.test",
    "aws_autoscaling_group.test"
  ]
  
  # Exclude all critical resources
  excluded_resources = [
    "aws_rds_instance.production",
    "aws_s3_bucket.production-data",
    "aws_dynamodb_table.critical",
    "aws_lambda.critical-function"
  ]
  
  # Only run during maintenance windows
  chaos_schedule = "weekdays"
  
  # Always backup before destruction
  backup_before_destruction = true
  
  # High minimum age to avoid new resources
  min_resource_age_hours = 24
  
  # Only resources with specific tags
  chaos_tags = {
    Environment = "test"
    ChaosAllowed = "true"
  }
  
  # Exclude production regions
  excluded_regions = [
    "us-east-1",
    "us-west-2"
  ]
  
  # Short duration limit
  chaos_duration_minutes = 10
}

# Safety outputs
output "production_safety_check" {
  value = "✅ Chaos monkey is safely disabled in production"
}

output "chaos_configuration" {
  value = {
    enabled = module.chaos_monkey.chaos_status.enabled
    safety_measures = [
      "Low destruction probability (1%)",
      "Maximum 1 destruction per run",
      "Critical resources excluded",
      "Maintenance window scheduling",
      "24-hour minimum resource age",
      "Tag-based filtering",
      "Region exclusions",
      "Short duration limits"
    ]
  }
}
