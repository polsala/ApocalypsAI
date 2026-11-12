# Data source for availability zones
data "aws_availability_zones" "available" {
  state = "available"
}

# VPC
resource "aws_vpc" "beacon_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "beacon-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "beacon_igw" {
  vpc_id = aws_vpc.beacon_vpc.id

  tags = {
    Name = "beacon-igw"
  }
}

# Public Subnets (for ALB)
resource "aws_subnet" "public_subnet" {
  count                   = 2 # Deploy in 2 AZs for high availability
  vpc_id                  = aws_vpc.beacon_vpc.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "beacon-public-subnet-${count.index}"
  }
}

# Private Subnets (for EC2 instances)
resource "aws_subnet" "private_subnet" {
  count                   = 2
  vpc_id                  = aws_vpc.beacon_vpc.id
  cidr_block              = "10.0.${count.index + 10}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = false

  tags = {
    Name = "beacon-private-subnet-${count.index}"
  }
}

# Route Table for Public Subnets
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.beacon_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.beacon_igw.id
  }

  tags = {
    Name = "beacon-public-rt"
  }
}

resource "aws_route_table_association" "public_rt_assoc" {
  count          = length(aws_subnet.public_subnet)
  subnet_id      = aws_subnet.public_subnet[count.index].id
  route_table_id = aws_route_table.public_rt.id
}

# EIP for NAT Gateway
resource "aws_eip" "nat_eip" {
  count = 2 # One EIP per NAT Gateway in each public subnet
  vpc   = true

  tags = {
    Name = "beacon-nat-eip-${count.index}"
  }
}

# NAT Gateway (for private instances to access internet for updates/packages)
resource "aws_nat_gateway" "beacon_nat_gw" {
  count         = 2
  allocation_id = aws_eip.nat_eip[count.index].id
  subnet_id     = aws_subnet.public_subnet[count.index].id

  tags = {
    Name = "beacon-nat-gw-${count.index}"
  }
  depends_on = [aws_internet_gateway.beacon_igw]
}

# Route Table for Private Subnets
resource "aws_route_table" "private_rt" {
  count  = 2
  vpc_id = aws_vpc.beacon_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.beacon_nat_gw[count.index].id
  }

  tags = {
    Name = "beacon-private-rt-${count.index}"
  }
}

resource "aws_route_table_association" "private_rt_assoc" {
  count          = length(aws_subnet.private_subnet)
  subnet_id      = aws_subnet.private_subnet[count.index].id
  route_table_id = aws_route_table.private_rt[count.index].id
}

# Security Group for ALB
resource "aws_security_group" "alb_sg" {
  vpc_id      = aws_vpc.beacon_vpc.id
  name        = "beacon-alb-sg"
  description = "Allow HTTP access to ALB"

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

  tags = {
    Name = "beacon-alb-sg"
  }
}

# Security Group for EC2 instances
resource "aws_security_group" "ec2_sg" {
  vpc_id      = aws_vpc.beacon_vpc.id
  name        = "beacon-ec2-sg"
  description = "Allow HTTP access from ALB and SSH from anywhere (for debugging)"

  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  ingress { # Optional: for debugging/management
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Restrict this in production!
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "beacon-ec2-sg"
  }
}

# Application Load Balancer
resource "aws_lb" "beacon_lb" {
  name               = "beacon-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = [for subnet in aws_subnet.public_subnet : subnet.id]

  tags = {
    Name = "beacon-lb"
  }
}

resource "aws_lb_target_group" "beacon_tg" {
  name     = "beacon-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.beacon_vpc.id

  health_check {
    path                = "/"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }

  tags = {
    Name = "beacon-tg"
  }
}

resource "aws_lb_listener" "beacon_listener" {
  load_balancer_arn = aws_lb.beacon_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.beacon_tg.arn
  }
}

# IAM Role for EC2 instances (minimal permissions)
resource "aws_iam_role" "ec2_instance_role" {
  name = "beacon-ec2-role"

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

  tags = {
    Name = "beacon-ec2-role"
  }
}

resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "beacon-ec2-profile"
  role = aws_iam_role.ec2_instance_role.name
}

# Launch Template
resource "aws_launch_template" "beacon_lt" {
  name_prefix   = "beacon-lt"
  image_id      = var.ami_id
  instance_type = var.instance_type
  key_name      = "" # No SSH key by default, add if needed for debugging
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]
  user_data     = base64encode(file("${path.module}/user_data.sh"))
  iam_instance_profile {
    name = aws_iam_instance_profile.ec2_instance_profile.name
  }

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "CosmicBeaconInstance"
    }
  }
  tag_specifications {
    resource_type = "volume"
    tags = {
      Name = "CosmicBeaconVolume"
    }
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "beacon_asg" {
  name                      = "beacon-asg"
  vpc_zone_identifier       = [for subnet in aws_subnet.private_subnet : subnet.id]
  desired_capacity          = var.desired_capacity
  max_size                  = var.max_size
  min_size                  = var.min_size
  health_check_type         = "ELB"
  health_check_grace_period = 300 # 5 minutes

  launch_template {
    id      = aws_launch_template.beacon_lt.id
    version = "$LATEST"
  }

  target_group_arns = [aws_lb_target_group.beacon_tg.arn]

  tag {
    key                 = "Name"
    value               = "CosmicBeaconASG"
    propagate_at_launch = true
  }
}

# Auto Scaling Policy (Target Tracking for CPU Utilization)
resource "aws_autoscaling_policy" "beacon_scaling_policy" {
  name                   = "beacon-cpu-scaling-policy"
  policy_type            = "TargetTrackingScaling"
  autoscaling_group_name = aws_autoscaling_group.beacon_asg.name

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 50.0 # Target 50% CPU utilization
  }
}
