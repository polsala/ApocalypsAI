variable "name_prefix" {
  description = "A prefix for naming all resources created by the module."
  type        = string
  default     = "nomad-node"
}

variable "region" {
  description = "The AWS region to deploy resources in."
  type        = string
}

variable "ami_id" {
  description = "The ID of the Amazon Machine Image (AMI) to use for the instances."
  type        = string
}

variable "instance_type" {
  description = "The EC2 instance type to use (e.g., t3.micro)."
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "The name of the EC2 Key Pair for SSH access."
  type        = string
}

variable "vpc_security_group_ids" {
  description = "A list of security group IDs to associate with the instances."
  type        = list(string)
}

variable "subnet_ids" {
  description = "A list of subnet IDs where the instances will be launched."
  type        = list(string)
}

variable "min_size" {
  description = "The minimum number of instances in the Auto Scaling Group."
  type        = number
  default     = 1
}

variable "max_size" {
  description = "The maximum number of instances in the Auto Scaling Group."
  type        = number
  default     = 1
}

variable "desired_capacity" {
  description = "The desired number of instances in the Auto Scaling Group."
  type        = number
  default     = 1
}

variable "user_data" {
  description = "User data to provide when launching the instances."
  type        = string
  default     = null
}

variable "tags" {
  description = "A map of tags to apply to all resources created by the module."
  type        = map(string)
  default     = {}
}

resource "aws_launch_template" "nomad_node" {
  name_prefix   = "${var.name_prefix}-lt-"
  image_id      = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  vpc_security_group_ids = var.vpc_security_group_ids
  user_data     = var.user_data != null ? base64encode(var.user_data) : null

  tag_specifications {
    resource_type = "instance"
    tags          = merge(var.tags, {
      Name = "${var.name_prefix}-instance"
    })
  }

  tag_specifications {
    resource_type = "volume"
    tags          = merge(var.tags, {
      Name = "${var.name_prefix}-volume"
    })
  }

  tags = merge(var.tags, {
    Name = "${var.name_prefix}-launch-template"
  })
}

resource "aws_autoscaling_group" "nomad_node" {
  name                      = "${var.name_prefix}-asg"
  max_size                  = var.max_size
  min_size                  = var.min_size
  desired_capacity          = var.desired_capacity
  vpc_zone_identifier       = var.subnet_ids
  health_check_type         = "EC2"
  health_check_grace_period = 300

  launch_template {
    id      = aws_launch_template.nomad_node.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.name_prefix}-asg"
    propagate_at_launch = true
  }

  # Propagate all custom tags to instances
  dynamic "tag" {
    for_each = var.tags
    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

output "asg_name" {
  description = "The name of the created Auto Scaling Group."
  value       = aws_autoscaling_group.nomad_node.name
}

output "launch_template_id" {
  description = "The ID of the created Launch Template."
  value       = aws_launch_template.nomad_node.id
}

output "launch_template_version" {
  description = "The version of the created Launch Template."
  value       = aws_launch_template.nomad_node.latest_version
}
