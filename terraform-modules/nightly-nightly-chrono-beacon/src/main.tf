resource "aws_security_group" "chrono_beacon_lb_sg" {
  name        = "chrono-beacon-lb-sg"
  description = "Allow HTTP traffic to Chrono Beacon ALB"
  vpc_id      = var.vpc_id

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
    Name = "chrono-beacon-lb-sg"
  }
}

resource "aws_security_group" "chrono_beacon_instance_sg" {
  name        = "chrono-beacon-instance-sg"
  description = "Allow HTTP traffic from ALB to Chrono Beacon instances"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.chrono_beacon_lb_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "chrono-beacon-instance-sg"
  }
}

resource "aws_lb" "chrono_beacon_lb" {
  name               = "chrono-beacon-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.chrono_beacon_lb_sg.id]
  subnets            = var.subnet_ids

  enable_deletion_protection = false

  tags = {
    Name = "chrono-beacon-lb"
  }
}

resource "aws_lb_target_group" "chrono_beacon_tg" {
  name     = "chrono-beacon-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

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
    Name = "chrono-beacon-tg"
  }
}

resource "aws_lb_listener" "chrono_beacon_listener" {
  load_balancer_arn = aws_lb.chrono_beacon_lb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.chrono_beacon_tg.arn
  }
}

data "aws_ami" "amazon_linux_2" {
  count       = var.ami_id == null ? 1 : 0
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_launch_template" "chrono_beacon_lt" {
  name_prefix   = "chrono-beacon-lt-"
  image_id      = var.ami_id != null ? var.ami_id : data.aws_ami.amazon_linux_2[0].id
  instance_type = var.instance_type

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.chrono_beacon_instance_sg.id]
  }

  user_data = base64encode(file("${path.module}/user_data.sh"))

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "chrono-beacon-instance"
    }
  }

  tags = {
    Name = "chrono-beacon-launch-template"
  }
}

resource "aws_autoscaling_group" "chrono_beacon_asg" {
  name                = "chrono-beacon-asg"
  vpc_zone_identifier = var.subnet_ids
  desired_capacity    = var.desired_capacity
  min_size            = var.min_size
  max_size            = var.max_size

  launch_template {
    id      = aws_launch_template.chrono_beacon_lt.id
    version = "$Latest"
  }

  target_group_arns = [aws_lb_target_group.chrono_beacon_tg.arn]

  tag {
    key                 = "Name"
    value               = "chrono-beacon-asg-instance"
    propagate_at_launch = true
  }
}
