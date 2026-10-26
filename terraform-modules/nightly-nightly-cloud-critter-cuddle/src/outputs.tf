output "instance_id" {
  description = "The ID of the provisioned EC2 instance."
  value       = aws_instance.critter.id
}

output "s3_bucket_name" {
  description = "The name of the provisioned S3 bucket."
  value       = aws_s3_bucket.critter_data.bucket
}

output "security_group_id" {
  description = "The ID of the security group created for the instance."
  value       = aws_security_group.critter_sg.id
}
