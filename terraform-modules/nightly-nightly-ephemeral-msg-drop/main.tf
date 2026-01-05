provider "aws" {
  region = var.aws_region
}

# Use default VPC and subnet for simplicity, or create new ones
data "aws_vpc" "selected" {
  default = true
}

data "aws_subnet_ids" "selected" {
  vpc_id = data.aws_vpc.selected.id
}

resource "aws_security_group" "message_drop_sg" {
  name        = "message-drop-sg-${random_string.suffix.result}"
  description = "Allow HTTP and SSH access to message drop"
  vpc_id      = data.aws_vpc.selected.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Be careful with this in production! Consider restricting to known IPs.
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "message-drop-sg"
  }
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

resource "aws_instance" "message_drop_instance" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = tolist(data.aws_subnet_ids.selected.ids)[0] # Pick first available subnet
  security_groups = [aws_security_group.message_drop_sg.name]
  associate_public_ip_address = true
  key_name      = var.key_pair_name # Optional, but good for debugging

  user_data = <<-EOF
            #!/bin/bash
            sudo apt-get update -y
            sudo apt-get install -y nginx
            echo "${var.message_content}" | sudo tee /var/www/html/index.html
            sudo systemctl start nginx
            sudo systemctl enable nginx
            echo "Instance will shut down in ${var.self_destruct_minutes} minutes."
            sudo shutdown -h +${var.self_destruct_minutes} & # Schedule shutdown in background
          EOF

  tags = {
    Name    = "EphemeralMessageDrop-${random_string.suffix.result}"
    Purpose = "ApocalypsAI-MessageDrop"
  }
}

output "public_ip" {
  value       = aws_instance.message_drop_instance.public_ip
  description = "The public IP address of the message drop instance."
}

output "public_dns" {
  value       = aws_instance.message_drop_instance.public_dns
  description = "The public DNS name of the message drop instance."
}

output "user_data_script_content" {
  value       = aws_instance.message_drop_instance.user_data
  description = "The generated user_data script content for testing."
  sensitive   = true # Mark as sensitive as it contains configuration details
}
