output "ec2_instance_id" {
  description = "The ID of the provisioned EC2 instance."
  value       = aws_instance.garden_instance.id
}

output "s3_bucket_id" {
  description = "The ID of the provisioned S3 bucket."
  value       = aws_s3_bucket.garden_bucket.id
}

output "rds_instance_address" {
  description = "The address of the provisioned RDS instance."
  value       = aws_db_instance.garden_db.address
}
