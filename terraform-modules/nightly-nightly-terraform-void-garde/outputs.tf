output "garden_url" {
  description = "The URL of the garden load balancer"
  value       = "http://${aws_lb.garden_alb.dns_name}"
}

output "easter_egg_path" {
  description = "The path to the hidden easter egg"
  value       = var.easter_egg_path
}
