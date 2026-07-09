output "beacon_url" {
  description = "The URL of the deployed sanctuary beacon webpage."
  value       = var.create_dns_record ? "http://${aws_route53_record.beacon_record[0].name}" : aws_s3_bucket_website_configuration.beacon_website.website_endpoint
}
