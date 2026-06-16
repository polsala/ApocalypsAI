variable "name_prefix" {
  description = "A prefix used for naming all resources."
  type        = string
  default     = "echo-chamber"
}

variable "region" {
  description = "The AWS region where resources will be deployed."
  type        = string
  default     = "us-east-1"
}
