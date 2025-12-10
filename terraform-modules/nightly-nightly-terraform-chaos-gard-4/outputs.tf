output "garden_summary" {
  description = "Summary of your chaos garden"
  value = {
    garden_name     = var.garden_name
    region          = var.region
    chaos_level     = var.chaos_level
    chaos_enabled   = var.enable_chaos
    bucket_name     = aws_s3_bucket.chaos_bucket.id
    lambda_name     = aws_lambda_function.chaos_lambda.function_name
    dashboard_url   = "https://console.aws.amazon.com/lambda/home?region=${var.region}#/functions/${aws_lambda_function.chaos_lambda.function_name}"
  }
}

output "chaos_instructions" {
  description = "Instructions for using your chaos garden"
  value = <<-EOT
    Your chaos garden has been planted! 🌱
    
    To monitor the chaos:
    1. Visit the Lambda dashboard: ${"https://console.aws.amazon.com/lambda/home?region=${var.region}#/functions/${aws_lambda_function.chaos_lambda.function_name}"}
    2. Check CloudWatch logs for chaos events
    3. Watch your S3 bucket for random objects
    
    Remember: This is a test environment. Chaos is expected and encouraged!
    
    Pro tip: Increase chaos_level for more unpredictable behavior.
  EOT
}
