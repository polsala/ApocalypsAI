output "s3_bucket_id" {
  description = "The ID (name) of the created S3 bucket."
  value       = aws_s3_bucket.celestial_bucket.id
}

output "s3_bucket_arn" {
  description = "The ARN of the created S3 bucket."
  value       = aws_s3_bucket.celestial_bucket.arn
}

output "constellation_map_entry" {
  description = "A formatted string representing the star map entry for this resource."
  value       = "Bucket '${aws_s3_bucket.celestial_bucket.id}' is charted as '${var.constellation_name}' at coordinates '${var.celestial_coordinates}'."
}
