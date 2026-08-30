output "public_ip" {
  description = "The public IP address of the Temporal Anomaly Outpost."
  value       = aws_instance.temporal_outpost.public_ip
}

output "instance_id" {
  description = "The ID of the EC2 instance."
  value       = aws_instance.temporal_outpost.id
}

output "security_group_id" {
  description = "The ID of the created security group."
  value       = aws_security_group.outpost_sg.id
}
