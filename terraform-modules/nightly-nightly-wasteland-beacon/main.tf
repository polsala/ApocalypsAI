resource "aws_vpc" "default" {
  cidr_block = "10.0.0.0/16"
  tags = merge(var.tags, {
    Name = "${var.tags["Project"]}-WastelandBeacon-VPC"
  })
}

resource "aws_subnet" "default" {
  vpc_id            = aws_vpc.default.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.region}a"
  tags = merge(var.tags, {
    Name = "${var.tags["Project"]}-WastelandBeacon-Subnet"
  })
}

resource "aws_internet_gateway" "default" {
  vpc_id = aws_vpc.default.id
  tags = merge(var.tags, {
    Name = "${var.tags["Project"]}-WastelandBeacon-IGW"
  })
}

resource "aws_route_table" "default" {
  vpc_id = aws_vpc.default.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.default.id
  }

  tags = merge(var.tags, {
    Name = "${var.tags["Project"]}-WastelandBeacon-RouteTable"
  })
}

resource "aws_route_table_association" "default" {
  subnet_id      = aws_subnet.default.id
  route_table_id = aws_route_table.default.id
}

resource "aws_security_group" "beacon_sg" {
  name        = "${var.tags["Project"]}-WastelandBeacon-SG"
  description = "Allow SSH and custom beacon port traffic"
  vpc_id      = aws_vpc.default.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow SSH from anywhere"
  }

  ingress {
    from_port   = var.beacon_port
    to_port     = var.beacon_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow custom beacon port from anywhere"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.tags["Project"]}-WastelandBeacon-SG"
  })
}

resource "aws_instance" "beacon_ec2" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  subnet_id     = aws_subnet.default.id
  vpc_security_group_ids = [aws_security_group.beacon_sg.id]
  associate_public_ip_address = true

  tags = merge(var.tags, {
    Name = "${var.tags["Project"]}-WastelandBeacon-EC2"
  })
}

resource "aws_s3_bucket" "beacon_storage" {
  bucket = "${lower(var.tags["Project"])}-${lower(replace(var.tags["BeaconName"], " ", "-"))}-wasteland-beacon-storage"
  acl    = "private" # Keep private by default, can be changed by user

  tags = merge(var.tags, {
    Name = "${var.tags["Project"]}-WastelandBeacon-S3"
  })
}

resource "aws_s3_bucket_public_access_block" "beacon_storage_block" {
  bucket = aws_s3_bucket.beacon_storage.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
