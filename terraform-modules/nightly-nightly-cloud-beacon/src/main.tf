terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

resource "aws_vpc" "beacon_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "apocalypsai-beacon-vpc"
  }
}

resource "aws_internet_gateway" "beacon_igw" {
  vpc_id = aws_vpc.beacon_vpc.id
  tags = {
    Name = "apocalypsai-beacon-igw"
  }
}

resource "aws_subnet" "beacon_subnet" {
  vpc_id            = aws_vpc.beacon_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.region}a" # Assuming 'a' zone exists
  map_public_ip_on_launch = true
  tags = {
    Name = "apocalypsai-beacon-subnet"
  }
}

resource "aws_route_table" "beacon_rt" {
  vpc_id = aws_vpc.beacon_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.beacon_igw.id
  }
  tags = {
    Name = "apocalypsai-beacon-rt"
  }
}

resource "aws_route_table_association" "beacon_rta" {
  subnet_id      = aws_subnet.beacon_subnet.id
  route_table_id = aws_route_table.beacon_rt.id
}

resource "aws_security_group" "beacon_sg" {
  vpc_id = aws_vpc.beacon_vpc.id
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTP access to the beacon"
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTPS access to the beacon (future proofing)"
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # WARNING: In a real scenario, restrict this to known IPs!
    description = "Allow SSH access (for maintenance)"
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "apocalypsai-beacon-sg"
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "beacon_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.beacon_subnet.id
  vpc_security_group_ids = [aws_security_group.beacon_sg.id]
  associate_public_ip_address = true # Will be replaced by EIP, but good for initial boot
  key_name = var.key_name == "" ? null : var.key_name # Only set if key_name is provided

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install -y nginx
              sudo systemctl start nginx
              sudo systemctl enable nginx
              echo "<html><body><h1>ApocalypsAI Cloud Beacon Active!</h1><p>${var.beacon_message}</p></body></html>" | sudo tee /var/www/html/index.html
              EOF

  tags = {
    Name = "apocalypsai-beacon-server"
  }
}

resource "aws_eip" "beacon_eip" {
  instance = aws_instance.beacon_server.id
  vpc      = true
  tags = {
    Name = "apocalypsai-beacon-eip"
  }
}

resource "aws_s3_bucket" "beacon_message_archive" {
  bucket = "apocalypsai-beacon-archive-${random_string.bucket_suffix.result}"
  acl    = "private" # Keep messages private by default
  tags = {
    Name = "apocalypsai-beacon-message-archive"
  }
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}
