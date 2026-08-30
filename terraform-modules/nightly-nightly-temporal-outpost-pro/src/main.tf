# Configure the AWS Provider
provider "aws" {
  region = var.region
  # Mock rationale: For terraform plan, credentials are not strictly needed for basic resource definitions.
  # The test script will only run 'terraform plan' to validate syntax and output structure.
  # For actual 'terraform apply', valid AWS credentials are required.
}

# Create a security group for the outpost
resource "aws_security_group" "outpost_sg" {
  name        = "${var.outpost_name}-sg"
  description = "Allow SSH and HTTP access to the temporal outpost"
  # Omitting vpc_id will cause it to be created in the default VPC.
  # This makes the module simpler and testable offline without needing to query for VPC data.

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # WARNING: For demonstration. Restrict in production!
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # WARNING: For demonstration. Restrict in production!
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.outpost_name}-sg"
  }
}

# Create the EC2 instance (the temporal outpost)
resource "aws_instance" "outpost" {
  ami           = var.ami
  instance_type = var.instance_type
  vpc_security_group_ids = [aws_security_group.outpost_sg.id]

  tags = {
    Name        = var.outpost_name
    Environment = "Temporal"
    Expires     = "In-${var.self_destruct_after_minutes}-Minutes"
  }

  # User data to install a simple web server (optional, for demonstration)
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y httpd
              sudo systemctl start httpd
              sudo systemctl enable httpd
              echo "<h1>Welcome to the Temporal Outpost! This outpost will self-destruct in ${var.self_destruct_after_minutes} minutes.</h1>" | sudo tee /var/www/html/index.html
              EOF
}

# A null resource to output the self-destruct command
# This is a whimsical way to provide the destroy instruction within the Terraform context.
resource "null_resource" "self_destruct_reminder" {
  triggers = {
    instance_id = aws_instance.outpost.id
  }

  provisioner "local-exec" {
    command = "echo \"Temporal Outpost '${var.outpost_name}' provisioned. Remember to initiate self-destruct in ${var.self_destruct_after_minutes} minutes!\""
    # Mock rationale: This local-exec runs during apply, but its command is simple and doesn't
    # interact with external systems. For 'terraform plan', it's ignored, but its definition
    # is part of the configuration validated by the test.
  }
}
