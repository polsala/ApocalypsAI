resource "aws_iam_role" "beacon_role" {
  name = "ephemeral-beacon-role-${var.region}"

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
}

resource "aws_iam_role_policy" "beacon_policy" {
  name = "ephemeral-beacon-policy-${var.region}"
  role = aws_iam_role.beacon_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:TerminateInstances",
          "s3:PutObject",
          "s3:GetBucketLocation"
        ]
        Effect   = "Allow"
        Resource = "*" # Consider scoping this down in a real scenario
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "*" # For CloudWatch logs if user data sends logs there
      }
    ]
  })
}

resource "aws_iam_instance_profile" "beacon_profile" {
  name = "ephemeral-beacon-profile-${var.region}"
  role = aws_iam_role.beacon_role.name
}

data "aws_ami" "selected_ami" {
  count = var.ami_id == null ? 1 : 0
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

locals {
  final_ami_id = var.ami_id != null ? var.ami_id : data.aws_ami.selected_ami[0].id
}

resource "aws_launch_template" "beacon_template" {
  name_prefix   = "ephemeral-beacon-"
  image_id      = local.final_ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  vpc_security_group_ids = var.security_group_ids
  iam_instance_profile {
    name = aws_iam_instance_profile.beacon_profile.name
  }

  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    task_script     = var.task_script,
    self_terminate  = var.self_terminate ? "true" : "false",
    log_bucket_name = var.log_bucket_name,
    region          = var.region
  }))

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name        = "ephemeral-beacon"
      ManagedBy   = "Terraform"
      Project     = "ApocalypsAI"
      BeaconType  = "Ephemeral"
    }
  }
}

resource "aws_ec2_instance" "beacon" {
  count = var.beacon_count

  launch_template {
    id      = aws_launch_template.beacon_template.id
    version = "$$Latest"
  }

  tags = {
    Name = "ephemeral-beacon-${count.index}"
  }
}
