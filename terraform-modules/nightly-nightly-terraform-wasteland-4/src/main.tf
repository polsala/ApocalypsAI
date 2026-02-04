variable "region" {
  type = string
}

variable "shelter_name" {
  type = string
}

provider "aws" {
  region = var.region
}

resource "aws_vpc" "shelter_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "${var.shelter_name}-vpc"
  }
}

resource "aws_subnet" "shelter_subnet" {
  vpc_id     = aws_vpc.shelter_vpc.id
  cidr_block = "10.0.1.0/24"
  tags = {
    Name = "${var.shelter_name}-subnet"
  }
}

resource "aws_instance" "shelter_instance" {
  ami           = "ami-0c55b159cbfafe1d0" # Ubuntu 20.04 LTS
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.shelter_subnet.id

  tags = {
    Name = "${var.shelter_name}-instance"
  }
}

resource "aws_s3_bucket" "survival_cache" {
  bucket = "${var.shelter_name}-survival-cache"
}

output "shelter_instance" {
  value = aws_instance.shelter_instance.public_ip
}

output "survival_bucket" {
  value = aws_s3_bucket.survival_cache.bucket
}
