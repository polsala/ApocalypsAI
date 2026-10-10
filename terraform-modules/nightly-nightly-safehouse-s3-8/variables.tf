variable "bucket_name" {
  description = "Name of the S3 bucket to create."
  type        = string
}

variable "ssm_parameter_name" {
  description = "Name of the SSM Parameter Store entry for the generated password."
  type        = string
}
