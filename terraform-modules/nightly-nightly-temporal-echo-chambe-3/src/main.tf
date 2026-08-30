provider "aws" {
  region = var.region
}

resource "aws_vpc" "echo_chamber_vpc" {
  cidr_block = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(var.tags, {
    Name = "${var.tags["Project"] == null ? "" : "${var.tags["Project"]}-"}TemporalEchoChamber-VPC"
  })
}

resource "aws_internet_gateway" "echo_chamber_igw" {
  vpc_id = aws_vpc.echo_chamber_vpc.id

  tags = merge(var.tags, {
    Name = "${var.tags["Project"] == null ? "" : "${var.tags["Project"]}-"}TemporalEchoChamber-IGW"
  })
}

resource "aws_subnet" "echo_chamber_subnet" {
  vpc_id            = aws_vpc.echo_chamber_vpc.id
  cidr_block        = var.subnet_cidr
  map_public_ip_on_launch = true
  availability_zone = "${var.region}a" # Using 'a' for simplicity, could be dynamic

  tags = merge(var.tags, {
    Name = "${var.tags["Project"] == null ? "" : "${var.tags["Project"]}-"}TemporalEchoChamber-Subnet"
  })
}

resource "aws_route_table" "echo_chamber_rt" {
  vpc_id = aws_vpc.echo_chamber_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.echo_chamber_igw.id
  }

  tags = merge(var.tags, {
    Name = "${var.tags["Project"] == null ? "" : "${var.tags["Project"]}-"}TemporalEchoChamber-RT"
  })
}

resource "aws_route_table_association" "echo_chamber_rta" {
  subnet_id      = aws_subnet.echo_chamber_subnet.id
  route_table_id = aws_route_table.echo_chamber_rt.id
}

resource "aws_security_group" "echo_chamber_sg" {
  name        = "${var.tags["Project"] == null ? "" : "${var.tags["Project"]}-"}temporal-echo-chamber-sg"
  description = "Allow SSH inbound traffic"
  vpc_id      = aws_vpc.echo_chamber_vpc.id

  ingress {
    description = "SSH from allowed CIDR"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.tags["Project"] == null ? "" : "${var.tags["Project"]}-"}TemporalEchoChamber-SG"
  })
}

resource "aws_instance" "echo_chamber_instance" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  subnet_id     = aws_subnet.echo_chamber_subnet.id
  vpc_security_group_ids = [aws_security_group.echo_chamber_sg.id]

  associate_public_ip_address = true

  tags = merge(var.tags, {
    Name = "${var.tags["Project"] == null ? "" : "${var.tags["Project"]}-"}TemporalEchoChamber-Instance"
  })
}
