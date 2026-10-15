resource "aws_vpc" "workshop_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "${var.project_name}-vpc"
    Environment = "whimsical-workshop"
  }
}

resource "aws_internet_gateway" "workshop_igw" {
  vpc_id = aws_vpc.workshop_vpc.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

resource "aws_subnet" "workshop_subnet" {
  vpc_id            = aws_vpc.workshop_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-subnet"
  }
}

resource "aws_route_table" "workshop_route_table" {
  vpc_id = aws_vpc.workshop_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.workshop_igw.id
  }

  tags = {
    Name = "${var.project_name}-route-table"
  }
}

resource "aws_route_table_association" "workshop_rta" {
  subnet_id      = aws_subnet.workshop_subnet.id
  route_table_id = aws_route_table.workshop_route_table.id
}

resource "aws_security_group" "workshop_sg" {
  vpc_id      = aws_vpc.workshop_vpc.id
  name        = "${var.project_name}-sg"
  description = "Allow SSH and HTTP access to whimsical widget instance"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow SSH from anywhere"
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTP from anywhere"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "${var.project_name}-sg"
  }
}

resource "aws_instance" "whimsical_widget_host" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.workshop_subnet.id
  vpc_security_group_ids = [aws_security_group.workshop_sg.id]
  associate_public_ip_address = true
  key_name      = var.ssh_key_name

  tags = {
    Name        = "${var.project_name}-widget-host"
    Environment = "whimsical-workshop"
  }
}
