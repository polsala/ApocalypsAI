variable "name" {
  description = "Name of the security group"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID where the security group will be created"
  type        = string
}

variable "rule_count" {
  description = "Number of random ingress rules to create"
  type        = number
  default     = 1
}

resource "aws_security_group" "void_bridge" {
  name        = var.name
  description = "Whimsical void bridge security group"
  vpc_id      = var.vpc_id
}

resource "aws_security_group_rule" "ingress" {
  count             = var.rule_count
  type              = "ingress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = [cidrsubnet("10.0.0.0/8", 8, count.index)]
  security_group_id = aws_security_group.void_bridge.id
  description       = "Random void rule ${count.index}"
}
