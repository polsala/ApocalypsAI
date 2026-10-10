variable "bucket_name" {
  description = "Name of the S3 bucket to create."
  type        = string
}

variable "create_supply_object" {
  description = "Whether to create a starter supply.txt object."
  type        = bool
  default     = true
}

variable "supply_content" {
  description = "Content of the starter supply object."
  type        = string
  default     = "Emergency supplies"
}
