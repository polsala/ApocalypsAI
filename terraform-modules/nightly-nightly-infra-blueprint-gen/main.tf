resource "aws_instance" "web_server" {
  ami           = var.ami_id
  instance_type = var.instance_type
  tags = {
    Name = "Web Server Instance"
  }

  vpc_security_group_ids = [aws_security_group.web_sg.id]
}

resource "aws_security_group" "web_sg" {
  name        = "web-server-sg"
  description = "Allow SSH and HTTP inbound traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
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
    Name = "Web Server Security Group"
  }
}

resource "aws_s3_bucket" "web_content" {
  bucket = var.bucket_name
  acl    = "public-read"

  tags = {
    Name = "Web Content Bucket"
  }
}

output "instance_id" {
  description = "The ID of the created EC2 instance."
  value       = aws_instance.web_server.id
}

output "security_group_id" {
  description = "The ID of the created security group."
  value       = aws_security_group.web_sg.id
}

output "bucket_name" {
  description = "The name of the created S3 bucket."
  value       = aws_s3_bucket.web_content.bucket
}
