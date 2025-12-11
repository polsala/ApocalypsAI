output "garden_resources" {
  description = "Map of created chaos garden resources"
  value = {
    ec2_instances = {
      count = var.create_ec2_instances ? var.ec2_instance_count : 0
      ids   = aws_instance.chaos_instances.*.id
      names = aws_instance.chaos_instances.*.tags.Name
    }
    lambda_functions = {
      count = var.create_lambda_functions ? var.lambda_function_count : 0
      names = aws_lambda_function.chaos_pollinators.*.function_name
      arns  = aws_lambda_function.chaos_pollinators.*.arn
    }
    s3_buckets = {
      count = var.create_s3_buckets ? var.s3_bucket_count : 0
      names = aws_s3_bucket.chaos_buckets.*.bucket
      arns  = aws_s3_bucket.chaos_buckets.*.arn
    }
    rds_instances = {
      count = var.create_rds_instances ? var.rds_instance_count : 0
      ids   = aws_db_instance.chaos_fertilizer.*.identifier
      arns  = aws_db_instance.chaos_fertilizer.*.arn
    }
    chaos_schedule = var.enable_chaos_experiments ? var.chaos_schedule : "disabled"
    cleanup_schedule = var.enable_automatic_cleanup ? var.cleanup_schedule : "disabled"
  }
}

output "chaos_schedule" {
  description = "The chaos experiment schedule expression"
  value       = var.enable_chaos_experiments ? var.chaos_schedule : "disabled"
}

output "cleanup_schedule" {
  description = "The cleanup job schedule expression"
  value       = var.enable_automatic_cleanup ? var.cleanup_schedule : "disabled"
}

output "dashboard_url" {
  description = "URL to the CloudWatch dashboard"
  value       = var.enable_cloudwatch_dashboard ? "https://console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#dashboards:name=${aws_cloudwatch_dashboard.chaos_garden_dashboard[0].dashboard_name}" : "disabled"
}

output "garden_name" {
  description = "The generated garden name"
  value       = random_pet.garden_name.id
}
