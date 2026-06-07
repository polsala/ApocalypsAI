output "vpc_id" {
  description = "The ID of the created VPC."
  value       = aws_vpc.echo_chamber_vpc.id
}

output "subnet_id" {
  description = "The ID of the created public subnet."
  value       = aws_subnet.echo_chamber_subnet.id
}

output "instance_public_ip" {
  description = "The public IP address of the EC2 instance."
  value       = aws_instance.echo_chamber_instance.public_ip
}

output "instance_id" {
  description = "The ID of the created EC2 instance."
  value       = aws_instance.echo_chamber_instance.id
}

output "security_group_id" {
  description = "The ID of the created security group."
  value       = aws_security_group.echo_chamber_sg.id
}
