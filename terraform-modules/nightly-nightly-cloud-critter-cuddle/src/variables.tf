variable "name" {
  description = "A unique name for the critter resources."
  type        = string
}

variable "instance_type" {
  description = "The EC2 instance type."
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance."
  type        = string
}

variable "key_name" {
  description = "The name of the EC2 Key Pair to use for the instance."
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC where the instance will be launched."
  type        = string
}

variable "subnet_id" {
  description = "The ID of the subnet where the instance will be launched."
  type        = string
}

variable "sleep_cron_expression" {
  description = "Cron expression for when the EC2 instance should stop (e.g., cron(0 22 * * ? *) for 10 PM UTC)."
  type        = string
}

variable "wake_cron_expression" {
  description = "Cron expression for when the EC2 instance should start (e.g., cron(0 8 * * ? *) for 8 AM UTC)."
  type        = string
}

variable "tags" {
  description = "A map of tags to assign to all resources."
  type        = map(string)
  default     = {}
}
