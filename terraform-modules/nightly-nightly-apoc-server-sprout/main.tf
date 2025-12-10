resource "aws_instance" "survival_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = var.instance_type
  tags = {
    Name        = "${var.survival_role}-server"
    Apocalypse  = "Hardcore"
    Role        = var.survival_role
    SproutLevel = "${length(aws_instance.survival_server.*.id)}"
  }
}

output "server_ips" {
  value = aws_instance.survival_server.*.public_ip
  description = "Public IPs of survival servers"
}
