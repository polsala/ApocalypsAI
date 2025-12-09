output "module_info" {
  value = {
    name        = "nightly-terraform-void-shield"
    version     = "1.0.0"
    description = "Mock cloud firewall with randomized security groups"
  }
}

output "security_group_rules" {
  value = [
    {
      protocol    = "tcp"
      from_port   = random_integer.ssh_port.result
      to_port     = random_integer.ssh_port.result
      cidr_blocks = var.allow_ssh_from
    },
    {
      protocol    = "tcp"
      from_port   = random_integer.http_port.result
      to_port     = random_integer.http_port.result
      cidr_blocks = var.allow_http_from
    },
    {
      protocol    = "tcp"
      from_port   = random_integer.https_port.result
      to_port     = random_integer.https_port.result
      cidr_blocks = var.allow_https_from
    }
  ]
}
