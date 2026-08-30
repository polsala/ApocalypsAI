output "alb_dns_name" {
  description = "The DNS name of the Application Load Balancer for the beacon."
  value       = aws_lb.temporal_beacon_alb.dns_name
}
