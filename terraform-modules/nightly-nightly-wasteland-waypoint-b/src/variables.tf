variable "bucket_name" {
  description = "The name for the S3 bucket to store static content."
  type        = string
}

variable "region" {
  description = "The AWS region to deploy resources in."
  type        = string
}

variable "content_file_path" {
  description = "The local path to the index.html file to upload to the S3 bucket."
  type        = string
}
