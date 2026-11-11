output "vpc_id" {
  description = "The ID of the created VPC."
  value       = aws_vpc.workshop_vpc.id
}

output "public_ip" {
  description = "The public IP address of the EC2 instance."
  value       = aws_instance.whimsical_widget_host.public_ip
}

output "security_group_id" {
  description = "The ID of the security group for the EC2 instance."
  value       = aws_security_group.workshop_sg.id
}
