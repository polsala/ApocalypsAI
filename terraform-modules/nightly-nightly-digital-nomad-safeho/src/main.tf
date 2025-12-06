provider "aws" {
  region = var.region
}

resource "aws_vpc" "nomad_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "DigitalNomadSafehouse"
  }
}

resource "aws_subnet" "private_subnets" {
  count = 2
  vpc_id = aws_vpc.nomad_vpc.id
  cidr_block = cidrsubnet(aws_vpc.nomad_vpc.cidr_block, 8, count.index)
  availability_zone = element(var.azs, count.index)
}

resource "aws_security_group" "bastion" {
  name = "nomad-bastion"
  description = "Secure SSH access"
  vpc_id = aws_vpc.nomad_vpc.id

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    security_groups = [aws_security_group.web.id]
  }
}

resource "aws_instance" "bastion_host" {
  ami = "ami-0c55b159cb415dd59"
  instance_type = "t3.nano"
  vpc_security_group_ids = [aws_security_group.bastion.id]
  tags = {
    Name = "BastionHost"
  }
}

resource "aws_lb" "web" {
  name = "nomad-web-lb"
  internal = false
  load_balancer_type = "application"
  security_groups = [aws_security_group.web.id]
  subnets = aws_subnet.private_subnets[*].id
}

resource "aws_autoscaling_group" "web_servers" {
  name = "nomad-web-group"
  min_size = 2
  max_size = 4
  desired_capacity = 2
  vpc_zone_identifier = aws_subnet.private_subnets[*].id
}

output "web_url" {
  value = aws_lb.web.dns_name
}
