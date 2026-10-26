output "bucket_id" {
  description = "The ID of the created S3 bucket"
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The ARN of the created S3 bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "supply_url" {
  description = "HTTPS URL of the starter‑supply object"
  value       = "https://s3-${var.region}.amazonaws.com/${aws_s3_bucket.safehouse.id}/starter-supply.txt"
}
