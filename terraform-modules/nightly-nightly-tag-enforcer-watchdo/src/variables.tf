variable "rule_name" {
  description = "The name for the AWS Config Rule."
  type        = string
  default     = "nightly-required-tags-rule"
}

variable "rule_description" {
  description = "A description for the AWS Config Rule."
  type        = string
  default     = "Ensures specified tags are present on resources."
}

variable "required_tags" {
  description = "A map of key-value pairs representing the tags that must be present."
  type        = map(string)
  default     = {
    "Environment" = "production"
    "Project"     = "ApocalypsAI"
  }
}

variable "resource_types" {
  description = "A list of AWS resource types to which the Config Rule applies."
  type        = list(string)
  default     = [
    "AWS::EC2::Instance",
    "AWS::S3::Bucket"
  ]
}
