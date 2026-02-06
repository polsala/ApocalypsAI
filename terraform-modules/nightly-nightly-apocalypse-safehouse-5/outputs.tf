output "bucket_id" {
  description = "The ID of the created bucket"
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "ARN of the bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "initial_object_key" {
  description = "Key of the placeholder object (if created)"
  value       = var.create_initial_object ? aws_s3_object.initial_supply[0].key : null
}
