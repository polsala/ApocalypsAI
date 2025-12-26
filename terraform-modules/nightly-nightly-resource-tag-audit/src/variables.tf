variable "resources_to_audit" {
  description = "A list of objects, each with 'arn' and 'tags' attributes, representing AWS resources to audit."
  type = list(object({
    arn  = string
    tags = map(string)
  }))
  default = []
}

variable "required_tags" {
  description = "A map of tag keys and optional values that must be present on resources."
  type = map(string)
  default = {}
}
