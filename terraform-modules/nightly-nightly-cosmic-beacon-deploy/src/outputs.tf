output "beacon_url" {
  description = "The URL of the Cosmic Beacon."
  value       = aws_lb.beacon_lb.dns_name
}
