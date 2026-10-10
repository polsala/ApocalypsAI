variable "vpc_cidr_block" {
  description = "The CIDR block for the Virtual Private Cloud."
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr_block" {
  description = "The CIDR block for the subnet."
  type        = string
  default     = "10.0.1.0/24"
}

variable "region" {
  description = "The cloud provider region to deploy resources."
  type        = string
  default     = "us-east-1"
}
