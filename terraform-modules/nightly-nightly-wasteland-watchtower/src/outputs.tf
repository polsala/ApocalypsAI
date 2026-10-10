output "watchtower_public_ip" {
  description = "The public IP address of the Watchtower EC2 instance."
  value       = aws_instance.watchtower.public_ip
}

output "watchtower_public_dns" {
  description = "The public DNS name of the Watchtower EC2 instance."
  value       = aws_instance.watchtower.public_dns
}

output "watchtower_security_group_id" {
  description = "The ID of the security group attached to the Watchtower."
  value       = aws_security_group.watchtower_sg.id
}
