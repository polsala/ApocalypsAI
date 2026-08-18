output "beacon_url" {
  description = "The full URL of the Chrono-Beacon endpoint."
  value       = "http://${aws_lb.chrono_beacon_lb.dns_name}/"
}

output "load_balancer_dns_name" {
  description = "The DNS name of the Application Load Balancer."
  value       = aws_lb.chrono_beacon_lb.dns_name
}
