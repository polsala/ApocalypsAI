variable "region" {
  description = "AWS region to deploy resources into."
  type        = string
}

variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket names. Must be globally unique."
  type        = string
}

variable "enable_lambda_echo" {
  description = "Whether to deploy the Lambda function to echo object metadata to CloudWatch Logs."
  type        = bool
  default     = true
}

variable "tags" {
  description = "A map of tags to apply to all resources."
  type        = map(string)
  default     = {}
}
