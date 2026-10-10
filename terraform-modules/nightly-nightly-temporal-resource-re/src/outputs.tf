output "echo_instance_id" {
  description = "The ID of the created echo EC2 instance."
  value       = aws_instance.echo.id
}

output "echo_instance_public_ip" {
  description = "The public IP of the created echo EC2 instance."
  value       = aws_instance.echo.public_ip
}
