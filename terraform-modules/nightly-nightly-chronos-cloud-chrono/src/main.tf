data "aws_ami" "ubuntu" {
  # Mock rationale: We need a specific AMI for the EC2 instance.
  # Using a data source allows us to dynamically fetch the latest Ubuntu LTS AMI.
  # For offline testing, Terraform will simulate this lookup.
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["099720109477"] # Canonical
}

resource "aws_security_group" "ntp_sg" {
  name        = "chronos-chronometer-ntp-sg"
  description = "Allow NTP inbound traffic"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 123
    to_port     = 123
    protocol    = "udp"
    cidr_blocks = var.allowed_cidrs
    description = "Allow NTP from specified CIDRs"
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow SSH from anywhere for convenience, restrict in production
    description = "Allow SSH from anywhere (consider restricting in production)"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = merge(
    var.tags,
    {
      Name = "chronos-chronometer-ntp-sg"
    }
  )
}

resource "aws_instance" "ntp_server" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.ntp_sg.id]
  subnet_id              = var.subnet_id
  associate_public_ip_address = true

  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update -y
              sudo apt-get install -y ntp
              sudo systemctl enable ntp
              sudo systemctl start ntp
              echo "NTP server setup complete."
              EOF

  tags = merge(
    var.tags,
    {
      Name = "Chronos-Cloud-Chronometer-NTP-Server"
    }
  )
}
