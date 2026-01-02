output "bucket_id" {
  description = "The ID of the created S3 bucket."
  value       = aws_s3_bucket.safehouse.id
}

output "password_file" {
  description = "Path to the generated password file."
  value       = local_file.password_file.filename
}
