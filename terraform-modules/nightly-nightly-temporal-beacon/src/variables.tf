variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}

variable "vpc_id" {
  description = "The ID of the VPC where the beacon will be deployed."
  type        = string
}

variable "public_subnet_ids" {
  description = "A list of public subnet IDs (at least two for HA) for the ALB and EC2s."
  type        = list(string)
}

variable "instance_type" {
  description = "The EC2 instance type for the beacon servers."
  type        = string
  default     = "t2.micro"
}

variable "desired_capacity" {
  description = "The desired number of beacon instances in the Auto Scaling Group."
  type        = number
  default     = 2
}

variable "beacon_message" {
  description = "The whimsical message to display on the beacon's web page."
  type        = string
  default     = "Temporal Beacon Active!"
}

# Internal variable for naming consistency
variable "util_name" {
  description = "Internal utility name for resource tagging."
  type        = string
  default     = "nightly-temporal-beacon"
  # This is an internal variable to ensure consistent naming across resources
  # and should not typically be overridden by the user.
}
