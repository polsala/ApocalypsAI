output "bucket_id" {
  description = "The ID of the created bucket"
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The ARN of the created bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "supply_file_url" {
  description = "URL of the optional supply‑cache file (empty if not created)"
  value = var.create_supply_file ? "s3://${aws_s3_bucket.safehouse.id}/supply‑cache.txt" : ""
}
