variable "region" {
  type = string
}

variable "instance_count" {
  type    = number
  default = 1
}

variable "bucket_name" {
  type = string
}

provider "aws" {
  region = var.region
}

resource "random_pet" "survivor" {
  count = var.instance_count
  length = 2
  separator = "-"
  prefix = "survivor"
}

resource "aws_instance" "void_node" {
  count = var.instance_count
  ami           = "ami-080e1f13689e07408"
  instance_type = "t2.micro"
  tags = {
    Name = random_pet.survivor[count.index].id
  }
}

resource "aws_s3_bucket" "survival_cache" {
  bucket = var.bucket_name
}

resource "aws_security_group" "radio_silence" {
  name        = "radio-silence-sg"
  description = "Block all inbound traffic to simulate radio silence"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Deny all inbound traffic"
  }
}

output "instance_ids" {
  value = aws_instance.void_node[*].id
}

output "bucket_arn" {
  value = aws_s3_bucket.survival_cache.arn
}

output "security_group_id" {
  value = aws_security_group.radio_silence.id
}
