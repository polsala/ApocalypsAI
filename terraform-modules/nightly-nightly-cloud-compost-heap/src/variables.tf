variable "project_name" {
  description = "A unique name for the project, used for resource naming and tagging."
  type        = string
}

variable "region" {
  description = "The AWS region where resources will be deployed."
  type        = string
}

variable "enable_s3_compost_bucket" {
  description = "Whether to create an S3 bucket for composted items/reports."
  type        = bool
  default     = true
}

variable "enable_ebs_stale_volume_detector" {
  description = "Whether to create an AWS Config rule for unattached EBS volumes."
  type        = bool
  default     = true
}

variable "enable_ec2_stale_instance_detector" {
  description = "Whether to create an AWS Config rule for long-stopped EC2 instances."
  type        = bool
  default     = true
}

variable "stale_instance_age_days" {
  description = "Number of days an EC2 instance must be stopped to be considered stale."
  type        = number
  default     = 30
}

variable "tags" {
  description = "A map of tags to apply to all created resources."
  type        = map(string)
  default     = {}
}
