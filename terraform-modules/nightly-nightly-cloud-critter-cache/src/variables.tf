variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. Terraform will append a unique suffix."
  type        = string
  default     = "apocalypsai-critter-cache-"
}

variable "region" {
  description = "The AWS region to deploy the S3 bucket."
  type        = string
  default     = "us-east-1"
}

variable "critter_name" {
  description = "The name of the digital critter this cache is for."
  type        = string
  default     = "ApocalypsAI-Bot"
}

variable "comfort_message" {
  description = "The comforting message to store in the cache."
  type        = string
  default     = "You are doing great, little digital friend! Keep integrating."
}
