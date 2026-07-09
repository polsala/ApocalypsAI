variable "region" {
  description = "AWS region to deploy the beacon."
  type        = string
  default     = "us-east-1"
}

variable "beacon_message" {
  description = "The message to display on the sanctuary beacon webpage."
  type        = string
  default     = "All Clear! Sanctuary Found."
}

variable "create_dns_record" {
  description = "Whether to create a Route 53 A record for the beacon."
  type        = bool
  default     = false
}

variable "domain_name" {
  description = "The domain name for the Route 53 record (e.g., example.com). Required if create_dns_record is true."
  type        = string
  default     = "example.com"
}

variable "subdomain" {
  description = "The subdomain for the Route 53 record (e.g., beacon). Required if create_dns_record is true."
  type        = string
  default     = "beacon"
}
