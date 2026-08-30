output "bucket_arn" {
  description = "ARN of the created S3 bucket."
  value       = aws_s3_bucket.safehouse.arn
}

output "password_parameter_arn" {
  description = "ARN of the SSM Parameter storing the password."
  value       = aws_ssm_parameter.password.arn
}
