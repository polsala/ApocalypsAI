output "bucket_id" {
  description = "The ID of the created bucket."
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The ARN of the created bucket."
  value       = aws_s3_bucket.safehouse.arn
}

output "supply_object_key" {
  description = "Key of the supply object (if created)."
  value       = var.create_supply_object ? aws_s3_bucket_object.supply[0].key : null
}
