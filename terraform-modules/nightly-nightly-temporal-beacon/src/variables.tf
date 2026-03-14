variable "region" {
  description = "The AWS region to deploy the beacon in."
  type        = string
}

variable "instance_type" {
  description = "The EC2 instance type for the temporal beacon."
  type        = string
}

variable "ami_id" {
  description = "The AMI ID to use for the EC2 instance."
  type        = string
}

variable "beacon_name" {
  description = "A whimsical name for your temporal beacon."
  type        = string
}

variable "chronal_anchor_tag_value" {
  description = "The value for the ChronalAnchor tag, identifying its stabilization role."
  type        = string
}
