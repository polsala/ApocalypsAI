variable "region" {
  description = "AWS region for deployment"
  type        = string
}

variable "instance_type" {
  description = "Instance type (t2.micro recommended)"
  type        = string
  default     = "t2.micro"
}

variable "survival_role" {
  description = "Server role in post-apocalyptic scenario"
  type        = string
  default     = "Wasteland Beacon"
}
