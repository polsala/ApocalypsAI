variable "resource_name_prefix" {
  description = "A short prefix for the resource name (e.g., 'sentry', 'data-node')."
  type        = string
}

variable "resource_type" {
  description = "The type of resource (e.g., 'EC2-Instance', 'RDS-DB', 'S3-Bucket')."
  type        = string
}

variable "environment" {
  description = "The deployment environment (e.g., 'dev', 'prod', 'staging')."
  type        = string
}
