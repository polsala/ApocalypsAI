variable "aws_region" {
  description = "The AWS region where the resources will be deployed."
  type        = string
}

variable "instance_tags" {
  description = "A map of tags to identify the EC2 instances that should be managed by the sentinel."
  type        = map(string)
}

variable "stop_cron_schedule" {
  description = "The cron expression for when instances should enter their slumber (stop). Example: cron(0 22 * * ? *)"
  type        = string
}

variable "start_cron_schedule" {
  description = "The cron expression for when instances should awaken (start). Example: cron(0 7 * * ? *)"
  type        = string
}

variable "lambda_memory_size" {
  description = "The memory size for the AWS Lambda function in MB."
  type        = number
  default     = 128
}

variable "lambda_timeout" {
  description = "The timeout for the AWS Lambda function in seconds."
  type        = number
  default     = 60
}
