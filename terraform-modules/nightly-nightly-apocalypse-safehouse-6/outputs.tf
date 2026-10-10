output "bucket_id" {
  description = "The ID of the created bucket"
  value       = aws_s3_bucket.safehouse.id
}

output "bucket_arn" {
  description = "The ARN of the created bucket"
  value       = aws_s3_bucket.safehouse.arn
}

output "radiation_level" {
  description = "Randomly generated radiation level (1‑10)"
  value       = random_integer.radiation.result
}
