variable "bucket_name" {\n  description = "Custom bucket name (must be globally unique). If null, a random name is generated."
  type        = string\n  default     = null\n}\n\nvariable "tags" {\n  description = "A map of tags to assign to the bucket."
  type        = map(string)\n  default     = {}\n}\n\nvariable "region" {\n  description = "AWS region where the bucket will be created."
  type        = string\n  default     = "us-east-1"\n}\n
