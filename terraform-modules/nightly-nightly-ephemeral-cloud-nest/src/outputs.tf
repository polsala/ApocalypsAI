output "vpc_id" {
  description = "The ID of the created VPC."
  value       = aws_vpc.main.id
}

output "subnet_id" {
  description = "The ID of the created public subnet."
  value       = aws_subnet.public.id
}

output "security_group_id" {
  description = "The ID of the created security group."
  value       = aws_security_group.instance_sg.id
}

output "instance_id" {
  description = "The ID of the created EC2 instance."
  value       = aws_instance.nest_instance.id
}

output "instance_public_ip" {
  description = "The public IP address of the EC2 instance."
  value       = aws_instance.nest_instance.public_ip
}
