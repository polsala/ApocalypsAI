variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A unique suffix will be appended."
  type        = string
  default     = "apocalypsai-bunker"
}

variable "region" {
  description = "The AWS region where the S3 bucket will be created."
  type        = string
  default     = "us-east-1"
}

variable "tags" {
  description = "A map of tags to assign to the S3 bucket."
  type        = map(string)
  default     = {}
}

variable "glacier_transition_days" {
  description = "Number of days after which non-current versions transition to Glacier Deep Archive."
  type        = number
  default     = 30
}

variable "glacier_expiration_days" {
  description = "Number of days after which non-current versions expire from Glacier Deep Archive."
  type        = number
  default     = 365
}
