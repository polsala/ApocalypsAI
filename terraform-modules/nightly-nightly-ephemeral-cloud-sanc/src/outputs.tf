output "vpc_id" {
  description = "The ID of the created VPC."
  value       = aws_vpc.sanctuary_vpc.id
}

output "subnet_id" {
  description = "The ID of the created subnet."
  value       = aws_subnet.sanctuary_subnet.id
}

output "s3_bucket_name" {
  description = "The name of the created S3 bucket."
  value       = aws_s3_bucket.sanctuary_bucket.bucket
}
