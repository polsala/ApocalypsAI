output "bucket_name" {
  description = "Name of the secret wardrobe bucket"
  value       = aws_s3_bucket.wardrobe.id
}
