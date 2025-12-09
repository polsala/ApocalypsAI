variable "environment" {
  description = "Environment name (prefix for resources)"
  type        = string
  default     = "test"
}

variable "region" {
  description = "Cloud region"
  type        = string
  default     = "us-east-1"
}

variable "allow_ssh_from" {
  description = "CIDR blocks allowed to access SSH"
  type        = list(string)
  default     = ["127.0.0.1/32"]
}

variable "allow_http_from" {
  description = "CIDR blocks allowed to access HTTP"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "allow_https_from" {
  description = "CIDR blocks allowed to access HTTPS"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
