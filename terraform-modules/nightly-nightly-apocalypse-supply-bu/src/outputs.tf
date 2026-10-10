output "bucket_name" {
  description = "Name of the created S3 bucket"
  value       = aws_s3_bucket.supply_bucket.id
}

output "supply_object_key" {
  description = "Key of the placeholder supply list object"
  value       = aws_s3_bucket_object.supply_list.key
}
