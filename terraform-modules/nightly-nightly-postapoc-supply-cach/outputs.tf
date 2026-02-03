output "bucket_id" {
  description = "ID of the created bucket."
  value       = aws_s3_bucket.supply_bucket.id
}

output "bucket_arn" {
  description = "ARN of the created bucket."
  value       = aws_s3_bucket.supply_bucket.arn
}

output "supply_object_key" {
  description = "Key of the randomly generated supply object."
  value       = aws_s3_bucket_object.supply_object.key
}
