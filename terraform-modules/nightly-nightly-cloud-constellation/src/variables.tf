variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name. Will be combined with constellation name and a random suffix."
  type        = string
}

variable "constellation_name" {
  description = "The whimsical name of the constellation to tag the resource with."
  type        = string
}

variable "celestial_coordinates" {
  description = "The celestial coordinates (e.g., RA, Dec) to tag the resource with."
  type        = string
}

variable "region" {
  description = "The AWS region to deploy the S3 bucket in."
  type        = string
}
