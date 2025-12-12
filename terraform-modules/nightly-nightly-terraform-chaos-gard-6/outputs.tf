output "chaos_garden_id" {
  description = "Unique identifier for the chaos garden"
  value       = random_pet.chaos_garden_id.id
}

output "ec2_instance_ids" {
  description = "List of created EC2 instance IDs"
  value       = aws_instance.chaos_garden[*].id
}

output "s3_bucket_names" {
  description = "List of created S3 bucket names"
  value       = aws_s3_bucket.chaos_garden[*].id
}

output "rds_instance_ids" {
  description = "List of created RDS instance IDs"
  value       = aws_db_instance.chaos_garden[*].id
}

output "lambda_function_arns" {
  description = "List of created Lambda function ARNs"
  value       = aws_lambda_function.chaos_garden[*].arn
}

output "vpc_id" {
  description = "VPC ID for the chaos garden"
  value       = aws_vpc.chaos_garden.id
}

output "security_group_id" {
  description = "Security group ID for the chaos garden"
  value       = aws_security_group.chaos_garden.id
}

output "cloudwatch_dashboard_url" {
  description = "CloudWatch dashboard URL for monitoring"
  value       = "https://console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#dashboards:name=${var.environment}-chaos-garden-dashboard"
}
