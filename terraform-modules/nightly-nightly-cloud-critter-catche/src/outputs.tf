output "instance_id" {
  description = "The ID of the provisioned EC2 instance."
  value       = aws_instance.critter.id
}

output "public_ip" {
  description = "The public IP address of the critter."
  value       = aws_instance.critter.public_ip
}
