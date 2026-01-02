output "instance_public_ip" {
  description = "The public IP address of the Cloud Critter instance."
  value       = aws_instance.critter_instance.public_ip
}

output "instance_id" {
  description = "The ID of the Cloud Critter instance."
  value       = aws_instance.critter_instance.id
}

output "security_group_id" {
  description = "The ID of the security group created for the Cloud Critter."
  value       = aws_security_group.critter_sg.id
}
