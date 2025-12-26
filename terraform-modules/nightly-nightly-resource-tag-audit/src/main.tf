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

locals {
  # Filter resources that are missing any of the required tag keys or have incorrect values
  missing_tags_resources = [
    for resource in var.resources_to_audit : {
      arn              = resource.arn
      missing_tag_keys = [
        for key, value in var.required_tags : key
        if !contains(keys(resource.tags), key) || (value != "" && resource.tags[key] != value)
      ]
    } if length([ # Only include resources that actually have missing tags
      for key, value in var.required_tags : key
      if !contains(keys(resource.tags), key) || (value != "" && resource.tags[key] != value)
    ]) > 0
  ]
}

output "audit_report" {
  description = "A list of resources found to be missing required tags, including the ARN and the missing tag keys."
  value       = local.missing_tags_resources
}
