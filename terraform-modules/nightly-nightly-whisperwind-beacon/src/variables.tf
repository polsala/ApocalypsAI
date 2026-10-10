variable "region" {
  description = "AWS region to deploy resources into."
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type for the beacon."
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance. Must be a valid AMI for the chosen region (e.g., Amazon Linux 2 or Ubuntu)."
  type        = string
}

variable "key_name" {
  description = "EC2 Key Pair name for SSH access. Must exist in the chosen region."
  type        = string
}

variable "beacon_message" {
  description = "The message the beacon will broadcast via its web server."
  type        = string
  default     = "Echoing hope across the digital wasteland."
}

variable "beacon_port" {
  description = "The port on which the beacon web server will run."
  type        = number
  default     = 8080
  validation {
    condition     = var.beacon_port >= 1024 && var.beacon_port <= 65535
    error_message = "The beacon_port must be between 1024 and 65535 (non-privileged ports)."
  }
}

variable "tags" {
  description = "A map of tags to apply to all resources created by the module."
  type        = map(string)
  default     = {}
}
