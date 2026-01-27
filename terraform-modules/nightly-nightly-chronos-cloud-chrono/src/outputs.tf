output "ntp_server_ip" {
  description = "The public IP address of the deployed NTP server."
  value       = aws_instance.ntp_server.public_ip
}
