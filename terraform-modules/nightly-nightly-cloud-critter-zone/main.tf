resource "aws_instance" "critter_instance" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_pair_name
  vpc_security_group_ids = [aws_security_group.critter_sg.id]
  user_data     = templatefile("${path.module}/user_data.sh.tpl", {
    critter_name = var.critter_name
  })

  tags = {
    Name = "CloudCritter-${var.critter_name}"
  }
}

resource "aws_security_group" "critter_sg" {
  name        = "critter-security-group-${var.critter_name}"
  description = "Allow HTTP and SSH access to Cloud Critter"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Be cautious with this in production environments
  }

  ingress {
    from_port   = 80
    to_port     = 80
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
    Name = "CloudCritter-SG-${var.critter_name}"
  }
}
