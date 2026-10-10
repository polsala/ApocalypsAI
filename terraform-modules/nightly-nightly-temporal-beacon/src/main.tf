resource "aws_security_group" "alb_sg" {
  name        = "${var.util_name}-alb-sg"
  description = "Allow HTTP access to ALB"
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
    Name = "${var.util_name}-alb-sg"
  }
}

resource "aws_security_group" "ec2_sg" {
  name        = "${var.util_name}-ec2-sg"
  description = "Allow HTTP access from ALB to EC2 instances"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.util_name}-ec2-sg"
  }
}

resource "aws_lb" "temporal_beacon_alb" {
  name               = "${var.util_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = var.public_subnet_ids

  tags = {
    Name = "${var.util_name}-alb"
  }
}

resource "aws_lb_target_group" "temporal_beacon_tg" {
  name     = "${var.util_name}-tg"
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
    Name = "${var.util_name}-tg"
  }
}

resource "aws_lb_listener" "temporal_beacon_listener" {
  load_balancer_arn = aws_lb.temporal_beacon_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.temporal_beacon_tg.arn
  }
}

data "aws_ami" "amazon_linux_2" {
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

resource "aws_launch_template" "temporal_beacon_lt" {
  name_prefix   = "${var.util_name}-lt-"
  image_id      = data.aws_ami.amazon_linux_2.id
  instance_type = var.instance_type
  key_name      = "" # Consider adding a key_name variable if SSH access is desired

  network_interfaces {
    associate_public_ip_address = true
    security_groups             = [aws_security_group.ec2_sg.id]
  }

  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    beacon_message = var.beacon_message
  }))

  tags = {
    Name = "${var.util_name}-instance"
  }
}

resource "aws_autoscaling_group" "temporal_beacon_asg" {
  name                      = "${var.util_name}-asg"
  vpc_zone_identifier       = var.public_subnet_ids
  desired_capacity          = var.desired_capacity
  min_size                  = 1
  max_size                  = var.desired_capacity * 2 # Allow scaling up to double desired
  target_group_arns         = [aws_lb_target_group.temporal_beacon_tg.arn]
  health_check_type         = "ELB"
  health_check_grace_period = 300

  launch_template {
    id      = aws_launch_template.temporal_beacon_lt.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.util_name}-asg-instance"
    propagate_at_launch = true
  }
}
