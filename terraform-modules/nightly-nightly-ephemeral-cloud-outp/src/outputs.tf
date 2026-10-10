output "instance_id" {
  description = "The ID of the provisioned EC2 instance."
  value       = aws_instance.ephemeral_outpost.id
}

output "public_ip" {
  description = "The public IP address of the EC2 instance."
  value       = aws_instance.ephemeral_outpost.public_ip
}

output "private_key_pem" {
  description = "The generated private key in PEM format. Handle with extreme care!"
  value       = tls_private_key.ephemeral_key.private_key_pem
  sensitive   = true
}

output "security_group_id" {
  description = "The ID of the created security group."
  value       = aws_security_group.ephemeral_sg.id
}
