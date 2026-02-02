output "beacon_public_ips" {
  description = "A list of public IP addresses of the deployed ephemeral beacons."
  value       = aws_ec2_instance.beacon[*].public_ip
}

output "beacon_instance_ids" {
  description = "A list of instance IDs of the deployed ephemeral beacons."
  value       = aws_ec2_instance.beacon[*].id
}

output "beacon_iam_role_name" {
  description = "The name of the IAM role created for the beacons."
  value       = aws_iam_role.beacon_role.name
}
