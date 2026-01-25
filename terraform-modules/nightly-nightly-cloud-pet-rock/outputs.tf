output "bucket_id" {
  description = "The ID of the S3 bucket."
  value       = aws_s3_bucket.pet_rock_bucket.id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket."
  value       = aws_s3_bucket.pet_rock_bucket.arn
}

output "website_endpoint" {
  description = "The website endpoint of the S3 bucket if website hosting is enabled."
  value       = var.enable_website_hosting ? aws_s3_bucket_website_configuration.pet_rock_bucket_website[0].website_endpoint : null
}
