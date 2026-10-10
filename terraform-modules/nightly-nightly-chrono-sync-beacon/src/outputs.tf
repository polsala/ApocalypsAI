output "public_ip" {
  description = "The public IP address of the Chrono-Sync Beacon."
  value       = aws_instance.chrono_sync_beacon.public_ip
}

output "public_dns" {
  description = "The public DNS name of the Chrono-Sync Beacon."
  value       = aws_instance.chrono_sync_beacon.public_dns
}

output "security_group_id" {
  description = "The ID of the security group created for the Chrono-Sync Beacon."
  value       = aws_security_group.chrono_sync_beacon_sg.id
}
