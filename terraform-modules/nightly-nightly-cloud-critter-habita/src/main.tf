terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

data "aws_ami" "amazon_linux_2" {
  count       = var.ami_id == "" ? 1 : 0
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_security_group" "critter_sg" {
  name        = "${var.critter_name}-critter-sg"
  description = "Allow SSH access to critter habitat"
  vpc_id      = data.aws_vpc.default.id # Assumes a default VPC exists

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.critter_name}-CritterSG"
  }
}

resource "aws_instance" "critter_instance" {
  ami           = var.ami_id == "" ? data.aws_ami.amazon_linux_2[0].id : var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  vpc_security_group_ids = [aws_security_group.critter_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              set -e
              yum update -y
              yum install -y cronie # Ensure cron is installed

              mkdir -p /opt/critter
              cat << 'CRITTER_SCRIPT_EOF' > /opt/critter/chirp.sh
              #!/bin/bash
              CRITTER_NAME="${var.critter_name}"
              TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
              echo "[${TIMESTAMP}] ${CRITTER_NAME} chirps happily from its habitat!" >> /var/log/critter.log
CRITTER_SCRIPT_EOF
              chmod +x /opt/critter/chirp.sh

              # Add to cron to run every minute
              (crontab -l 2>/dev/null; echo "* * * * * CRITTER_NAME=\"${var.critter_name}\" /opt/critter/chirp.sh") | crontab -
              EOF

  tags = {
    Name = "${var.critter_name}-CritterHabitat"
  }
}

resource "aws_cloudwatch_log_group" "critter_log_group" {
  name              = "/aws/ec2/critter-habitat-${var.critter_name}"
  retention_in_days = 7

  tags = {
    Name = "${var.critter_name}-CritterLogs"
  }
}

data "aws_vpc" "default" {
  default = true
}
