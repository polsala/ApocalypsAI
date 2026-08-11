terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0" # Updated to a more recent version
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0" # Updated to a more recent version
    }
  }
}

resource "aws_vpc" "default" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "ephemeral-shelter-vpc-${var.name_prefix}"
  }
}

resource "aws_subnet" "default" {
  vpc_id            = aws_vpc.default.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.region}a"
  tags = {
    Name = "ephemeral-shelter-subnet-${var.name_prefix}"
  }
}

resource "aws_internet_gateway" "default" {
  vpc_id = aws_vpc.default.id
  tags = {
    Name = "ephemeral-shelter-igw-${var.name_prefix}"
  }
}

resource "aws_route_table" "default" {
  vpc_id = aws_vpc.default.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.default.id
  }
  tags = {
    Name = "ephemeral-shelter-rt-${var.name_prefix}"
  }
}

resource "aws_route_table_association" "default" {
  subnet_id      = aws_subnet.default.id
  route_table_id = aws_route_table.default.id
}

resource "aws_security_group" "shelter_sg" {
  name        = "ephemeral-shelter-sg-${var.name_prefix}"
  description = "Allow SSH inbound traffic"
  vpc_id      = aws_vpc.default.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # WARNING: For ephemeral use only, restrict in production!
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ephemeral-shelter-sg-${var.name_prefix}"
  }
}

resource "tls_private_key" "ssh" {
  count     = var.create_key_pair ? 1 : 0
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "generated_key" {
  count      = var.create_key_pair ? 1 : 0
  key_name   = "ephemeral-shelter-key-${var.name_prefix}"
  public_key = tls_private_key.ssh[0].public_key_openssh
}

resource "aws_instance" "shelter_instance" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.default.id
  vpc_security_group_ids = [aws_security_group.shelter_sg.id]
  key_name      = var.create_key_pair ? aws_key_pair.generated_key[0].key_name : var.ssh_key_name

  tags = merge(
    {
      Name = "ephemeral-shelter-instance-${var.name_prefix}"
    },
    var.tags
  )
}
