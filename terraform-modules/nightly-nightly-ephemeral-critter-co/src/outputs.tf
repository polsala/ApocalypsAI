# outputs.tf - Output variables from the module

output "instance_id" {
  description = "The ID of the provisioned EC2 critter instance."
  value       = aws_instance.critter.id
}

output "public_ip" {
  description = "The public IP address of the EC2 critter instance (if available)."
  value       = aws_instance.critter.public_ip
}
