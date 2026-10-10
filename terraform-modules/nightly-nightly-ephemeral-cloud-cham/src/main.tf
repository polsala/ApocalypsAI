resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = merge(var.tags, {
    Name = "ephemeral-cloud-chamber-vpc"
  })
}

resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a" # Simple for ephemeral
  tags = merge(var.tags, {
    Name = "ephemeral-cloud-chamber-subnet"
  })
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = merge(var.tags, {
    Name = "ephemeral-cloud-chamber-igw"
  })
}

resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  tags = merge(var.tags, {
    Name = "ephemeral-cloud-chamber-rt"
  })
}

resource "aws_route_table_association" "main" {
  subnet_id      = aws_subnet.main.id
  route_table_id = aws_route_table.main.id
}

resource "aws_security_group" "instance_sg" {
  name        = "ephemeral-instance-sg"
  description = "Allow HTTP/SSH for ephemeral instance"
  vpc_id      = aws_vpc.main.id

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

  tags = merge(var.tags, {
    Name = "ephemeral-instance-sg"
  })
}

data "aws_ami" "ubuntu" {
  count       = var.ami_id == null ? 1 : 0 # Only fetch if ami_id is not provided
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

resource "aws_instance" "ephemeral_server" {
  ami           = var.ami_id != null ? var.ami_id : data.aws_ami.ubuntu[0].id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.main.id
  vpc_security_group_ids = [aws_security_group.instance_sg.id]
  associate_public_ip_address = true # For easy access in ephemeral setup

  tags = merge(var.tags, {
    Name = "ephemeral-chamber-server"
  })
}

resource "aws_s3_bucket" "ephemeral_storage" {
  bucket = "${var.bucket_name_prefix}-${random_id.bucket_suffix.hex}"
  acl    = "private" # Best practice

  tags = merge(var.tags, {
    Name = "ephemeral-chamber-storage"
  })
}

resource "random_id" "bucket_suffix" {
  byte_length = 8
}
