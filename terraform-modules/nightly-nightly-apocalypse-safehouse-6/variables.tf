variable "bucket_name" {
  description = "Optional custom bucket name. If empty, a random whimsical name is generated."
  type        = string
  default     = ""
}

variable "tags" {
  description = "A map of tags to assign to the bucket."
  type        = map(string)
  default     = {}
}
