output "bucket_id" {
  description = "The name (ID) of the created bucket"
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "ARN of the bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "supply_object_key" {
  description = "Key of the optional supply object (empty string if not created)"
  value       = var.create_supply ? aws_s3_bucket_object.supply[0].key : ""
}
