variable "region" {
  description = "The AWS region to scan for unattached EBS volumes."
  type        = string
  default     = "us-east-1"
}

variable "tags_filter" {
  description = "A map of tags to filter EBS volumes. Only volumes matching these tags will be considered. Empty map means no tag filtering."
  type        = map(string)
  default     = {}
}
