output "instance_id" {
  description = "The ID of the deployed EC2 instance."
  value       = aws_instance.temporal_beacon.id
}

output "public_ip" {
  description = "The public IP address of the EC2 instance."
  value       = aws_instance.temporal_beacon.public_ip
}
