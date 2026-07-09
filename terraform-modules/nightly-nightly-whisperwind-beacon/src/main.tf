resource "aws_vpc" "default" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = merge(var.tags, {
    Name = "whisperwind-beacon-vpc"
  })
}

resource "aws_subnet" "default" {
  vpc_id     = aws_vpc.default.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "${var.region}a"
  tags = merge(var.tags, {
    Name = "whisperwind-beacon-subnet"
  })
}

resource "aws_internet_gateway" "default" {
  vpc_id = aws_vpc.default.id
  tags = merge(var.tags, {
    Name = "whisperwind-beacon-igw"
  })
}

resource "aws_route_table" "default" {
  vpc_id = aws_vpc.default.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.default.id
  }
  tags = merge(var.tags, {
    Name = "whisperwind-beacon-rt"
  })
}

resource "aws_route_table_association" "default" {
  subnet_id      = aws_subnet.default.id
  route_table_id = aws_route_table.default.id
}

resource "aws_security_group" "beacon_sg" {
  name        = "whisperwind-beacon-sg"
  description = "Allow SSH and beacon port inbound traffic"
  vpc_id      = aws_vpc.default.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # WARNING: For production, restrict this to known IPs
    description = "Allow SSH access"
  }

  ingress {
    from_port   = var.beacon_port
    to_port     = var.beacon_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # WARNING: For production, restrict this to known IPs
    description = "Allow beacon service access"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = merge(var.tags, {
    Name = "whisperwind-beacon-sg"
  })
}

resource "aws_s3_bucket" "beacon_logs" {
  bucket = "whisperwind-beacon-logs-${random_id.bucket_suffix.hex}"
  acl    = "private" # Ensure bucket is private by default

  tags = merge(var.tags, {
    Name = "whisperwind-beacon-logs"
  })
}

resource "random_id" "bucket_suffix" {
  byte_length = 8
}

resource "aws_iam_role" "beacon_instance_role" {
  name = "whisperwind-beacon-instance-role-${random_id.role_suffix.hex}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })

  tags = merge(var.tags, {
    Name = "whisperwind-beacon-instance-role"
  })
}

resource "random_id" "role_suffix" {
  byte_length = 4
}

resource "aws_iam_role_policy" "beacon_s3_access_policy" {
  name = "whisperwind-beacon-s3-access-policy"
  role = aws_iam_role.beacon_instance_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket",
        ]
        Effect = "Allow"
        Resource = [
          aws_s3_bucket.beacon_logs.arn,
          "${aws_s3_bucket.beacon_logs.arn}/*",
        ]
      },
    ]
  })
}

resource "aws_iam_instance_profile" "beacon_instance_profile" {
  name = "whisperwind-beacon-instance-profile-${random_id.profile_suffix.hex}"
  role = aws_iam_role.beacon_instance_role.name
}

resource "random_id" "profile_suffix" {
  byte_length = 4
}

resource "aws_instance" "beacon" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  vpc_security_group_ids = [aws_security_group.beacon_sg.id]
  subnet_id     = aws_subnet.default.id
  associate_public_ip_address = true
  user_data     = templatefile("${path.module}/user_data.sh.tpl", {
    beacon_message = var.beacon_message
    beacon_port    = var.beacon_port
    s3_bucket_name = aws_s3_bucket.beacon_logs.bucket
    region         = var.region
  })

  iam_instance_profile = aws_iam_instance_profile.beacon_instance_profile.name

  tags = merge(var.tags, {
    Name = "Whisperwind Beacon"
  })
}
