provider "aws" {
  region = var.region
  # No actual credentials needed for plan validation, but provider block is required.
  # For actual deployment, AWS credentials must be configured in the environment
  # or via a credentials file.
}

resource "aws_security_group" "watchtower_sg" {
  name        = "nightly-watchtower-sg"
  description = "Security group for Nightly Wasteland Watchtower"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # WARNING: Restrict in production
    description = "Allow SSH access"
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # WARNING: Restrict in production
    description = "Allow HTTP access (e.g., for monitoring dashboard)"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "NightlyWastelandWatchtower-SG"
    ManagedBy = "ApocalypsAI"
  }
}

resource "aws_instance" "watchtower" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  vpc_security_group_ids = [aws_security_group.watchtower_sg.id]

  tags = {
    Name = "NightlyWastelandWatchtower"
    ManagedBy = "ApocalypsAI"
  }
}
