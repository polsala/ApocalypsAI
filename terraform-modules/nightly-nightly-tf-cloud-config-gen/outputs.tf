output "vpc_id" {
  description = "The ID of the created VPC."
  value       = aws_vpc.main.id
}

output "subnet_id" {
  description = "The ID of the created subnet."
  value       = aws_subnet.main.id
}
