variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. A random suffix will be appended."
  type        = string
  default     = "nightly-postbox"
}

variable "allowed_ip_cidrs" {
  description = "A list of IP CIDR blocks allowed to put objects into the bucket."
  type        = list(string)
  default     = ["0.0.0.0/0"] # WARNING: This default allows all IPs. Restrict this in production.
}

variable "region" {
  description = "The AWS region where the S3 bucket will be created."
  type        = string
  default     = "us-east-1"
}
