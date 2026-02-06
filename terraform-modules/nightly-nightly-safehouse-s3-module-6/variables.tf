variable "bucket_name" {
  description = "Optional explicit bucket name. If empty, a random name is generated."
  type        = string
  default     = ""
}

variable "force_destroy" {
  description = "Whether to allow force destroy of the bucket."
  type        = bool
  default     = false
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}
