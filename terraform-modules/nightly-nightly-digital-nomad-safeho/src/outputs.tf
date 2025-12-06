output "vpc_id" {
  description = "ID of the created VPC"
  value = aws_vpc.nomad_vpc.id
}

output "bastion_ip" {
  description = "Public IP of the bastion host"
  value = aws_instance.bastion_host.public_ip
}

output "web_url" {
  description = "URL of the web interface"
  value = "https://${aws_lb.web.dns_name}"
}
