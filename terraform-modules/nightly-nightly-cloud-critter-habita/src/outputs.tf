output "instance_public_ip" {
  description = "The public IP address of the deployed EC2 instance."
  value       = aws_instance.critter_instance.public_ip
}

output "log_group_name" {
  description = "The name of the CloudWatch Log Group where critter chirps are sent."
  value       = aws_cloudwatch_log_group.critter_log_group.name
}
