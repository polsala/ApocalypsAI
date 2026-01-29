variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-west-1"
}

variable "shelter_name" {
  description = "Name of the shelter"
  type        = string
  default     = "shelter"
}

variable "instance_type" {
  description = "Compute instance type"
  type        = string
  default     = "t3.micro"
}

variable "db_instance_class" {
  description = "Database instance class"
  type        = string
  default     = "db.t3.micro"
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

resource "aws_instance" "shelter_vm" {
  ami           = "ami-0c55b159cbfafe1d0" # Amazon Linux 2
  instance_type = var.instance_type
  subnet_id     = aws_subnet.shelter_subnet.id

  tags = {
    Name = var.shelter_name
  }
}

resource "aws_db_instance" "water_filtration_db" {
  identifier             = "${var.shelter_name}-db"
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = var.db_instance_class
  allocated_storage      = 20
  username               = "survivor"
  password               = "secure_wasteland123"
  publicly_accessible    = false
  skip_final_snapshot    = true
  vpc_security_group_ids = [aws_security_group.db_sg.id]
}

resource "aws_security_group" "db_sg" {
  name        = "${var.shelter_name}-db-sg"
  description = "Security group for water filtration DB"
  vpc_id      = aws_vpc.shelter_vpc.id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.shelter_vpc.cidr_block]
  }
}

output "shelter_ip" {
  value = aws_instance.shelter_vm.public_ip
}

output "db_endpoint" {
  value = aws_db_instance.water_filtration_db.endpoint
}

output "vpc_id" {
  value = aws_vpc.shelter_vpc.id
}
