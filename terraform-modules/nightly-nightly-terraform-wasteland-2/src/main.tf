variable "region" {
  type = string
}

variable "outpost_name" {
  type = string
}

variable "instance_count" {
  type    = number
  default = 1
}

provider "aws" {
  region = var.region
}

resource "aws_vpc" "outpost_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "${var.outpost_name}-vpc"
    Theme = "Wasteland"
    Purpose = "Survival Outpost"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.outpost_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.outpost_name}-public-subnet"
    Theme = "Wasteland"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.outpost_vpc.id

  tags = {
    Name = "${var.outpost_name}-igw"
    Theme = "Wasteland"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.outpost_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "${var.outpost_name}-public-rt"
    Theme = "Wasteland"
  }
}

resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_security_group" "outpost_sg" {
  name        = "${var.outpost_name}-sg"
  description = "Security group for wasteland outpost"
  vpc_id      = aws_vpc.outpost_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
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
    Name = "${var.outpost_name}-sg"
    Theme = "Wasteland"
  }
}

resource "aws_instance" "outpost_instance" {
  count         = var.instance_count
  ami           = "ami-0c55b159cbfafe1d0" # Amazon Linux 2
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.outpost_sg.id]

  tags = {
    Name = "${var.outpost_name}-node-${count.index}"
    Theme = "Wasteland"
    Role = "Scavenger Node"
  }
}

output "vpc_id" {
  value = aws_vpc.outpost_vpc.id
}

output "public_ips" {
  value = aws_instance.outpost_instance[*].public_ip
}
