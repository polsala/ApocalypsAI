resource "aws_key_pair" "ephemeral_key" {
  key_name   = var.key_name
  public_key = tls_private_key.ephemeral_key.public_key_openssh
}

resource "tls_private_key" "ephemeral_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "aws_security_group" "ephemeral_sg" {
  name        = "${var.instance_name}-sg"
  description = "Security group for ${var.instance_name}"
  vpc_id      = data.aws_vpc.default.id # Assumes a default VPC exists

  dynamic "ingress" {
    for_each = var.ingress_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.instance_name}-sg"
  }
}

resource "aws_instance" "ephemeral_outpost" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = aws_key_pair.ephemeral_key.key_name
  vpc_security_group_ids = [aws_security_group.ephemeral_sg.id]

  tags = {
    Name = var.instance_name
  }
}

data "aws_vpc" "default" {
  default = true
}
