terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

provider "aws" {
  region = var.region
}

variable "garden_name" {
  description = "Name of the garden"
  type        = string
  default     = "void-garden"
}

variable "environment" {
  description = "Environment tag"
  type        = string
  default     = "dev"
}

variable "max_instances" {
  description = "Maximum number of instances"
  type        = number
  default     = 3
}

variable "min_instances" {
  description = "Minimum number of instances"
  type        = number
  default     = 1
}

variable "desired_capacity" {
  description = "Desired number of instances"
  type        = number
  default     = 2
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

# Create a VPC
resource "aws_vpc" "garden_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "${var.garden_name}-vpc"
    Env  = var.environment
  }
}

# Create an internet gateway
resource "aws_internet_gateway" "garden_igw" {
  vpc_id = aws_vpc.garden_vpc.id
  tags = {
    Name = "${var.garden_name}-igw"
    Env  = var.environment
  }
}

# Create a subnet
resource "aws_subnet" "garden_subnet" {
  vpc_id                  = aws_vpc.garden_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  tags = {
    Name = "${var.garden_name}-subnet"
    Env  = var.environment
  }
}

# Create a route table
resource "aws_route_table" "garden_rt" {
  vpc_id = aws_vpc.garden_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.garden_igw.id
  }
  tags = {
    Name = "${var.garden_name}-rt"
    Env  = var.environment
  }
}

# Associate the subnet with the route table
resource "aws_route_table_association" "garden_rta" {
  subnet_id      = aws_subnet.garden_subnet.id
  route_table_id = aws_route_table.garden_rt.id
}

# Create a security group for the garden
resource "aws_security_group" "garden_sg" {
  name        = "${var.garden_name}-sg"
  description = "Security group for the whimsical garden"
  vpc_id      = aws_vpc.garden_vpc.id
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SSH access"
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP access"
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }
  tags = {
    Name = "${var.garden_name}-sg"
    Env  = var.environment
  }
}

# Create a launch template for the garden instances
resource "aws_launch_template" "garden_lt" {
  name_prefix   = "${var.garden_name}-lt-"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
  key_name      = var.key_name
  user_data     = base64encode(templatefile("${path.module}/user_data.sh", { easter_egg_path = var.easter_egg_path }))
  vpc_security_group_ids = [aws_security_group.garden_sg.id]
  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "${var.garden_name}-instance"
      Env  = var.environment
    }
  }
}

# Create an auto scaling group
resource "aws_autoscaling_group" "garden_asg" {
  name                      = "${var.garden_name}-asg"
  max_size                  = var.max_instances
  min_size                  = var.min_instances
  desired_capacity          = var.desired_capacity
  health_check_grace_period = 300
  health_check_type         = "EC2"
  force_delete              = true
  vpc_zone_identifier       = [aws_subnet.garden_subnet.id]
  launch_template {
    id      = aws_launch_template.garden_lt.id
    version = "$Latest"
  }
  tag {
    key                 = "Name"
    value               = "${var.garden_name}-instance"
    propagate_at_launch = true
  }
  tag {
    key                 = "Env"
    value               = var.environment
    propagate_at_launch = true
  }
}

# Create a target group
resource "aws_lb_target_group" "garden_tg" {
  name        = "${var.garden_name}-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.garden_vpc.id
  target_type = "instance"
  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
    path                = "/"
    matcher             = "200"
  }
  tags = {
    Name = "${var.garden_name}-tg"
    Env  = var.environment
  }
}

# Attach the auto scaling group to the target group
resource "aws_autoscaling_attachment" "garden_asg_tg" {
  autoscaling_group_name = aws_autoscaling_group.garden_asg.id
  lb_target_group_arn    = aws_lb_target_group.garden_tg.arn
}

# Create an application load balancer
resource "aws_lb" "garden_alb" {
  name               = "${var.garden_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.garden_sg.id]
  subnets            = [aws_subnet.garden_subnet.id]
  enable_deletion_protection = false
  tags = {
    Name = "${var.garden_name}-alb"
    Env  = var.environment
  }
}

# Create a listener for the load balancer
resource "aws_lb_listener" "garden_listener" {
  load_balancer_arn = aws_lb.garden_alb.arn
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.garden_tg.arn
  }
}

# Create a listener rule for the easter egg
resource "aws_lb_listener_rule" "garden_easter_egg" {
  listener_arn = aws_lb_listener.garden_listener.arn
  priority     = 100
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.garden_tg.arn
  }
  condition {
    path_pattern {
      values = ["${var.easter_egg_path}"]
    }
  }
}

# Create an SNS topic for alerts
resource "aws_sns_topic" "garden_alerts" {
  name = "${var.garden_name}-alerts"
  tags = {
    Name = "${var.garden_name}-alerts"
    Env  = var.environment
  }
}

# Create a CloudWatch alarm for high CPU usage
resource "aws_cloudwatch_metric_alarm" "garden_cpu_alarm" {
  alarm_name          = "${var.garden_name}-cpu-alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors ec2 cpu utilization"
  alarm_actions       = [aws_sns_topic.garden_alerts.arn]
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.garden_asg.name
  }
  tags = {
    Name = "${var.garden_name}-cpu-alarm"
    Env  = var.environment
  }
}

# Data source for the latest Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Output the garden URL
output "garden_url" {
  description = "The URL of the garden load balancer"
  value       = "http://${aws_lb.garden_alb.dns_name}"
}

# Output the easter egg path
output "easter_egg_path" {
  description = "The path to the hidden easter egg"
  value       = var.easter_egg_path
}

# Variable for the easter egg path
variable "easter_egg_path" {
  description = "Path to the hidden easter egg"
  type        = string
  default     = "/whimsical-void"
}

# Variable for the key pair name
variable "key_name" {
  description = "Name of the SSH key pair"
  type        = string
  default     = ""
}
