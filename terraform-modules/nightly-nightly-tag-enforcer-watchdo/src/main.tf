resource "aws_config_config_rule" "required_tags_rule" {
  name        = var.rule_name
  description = var.rule_description

  source {
    owner             = "AWS"
    source_identifier = "REQUIRED_TAGS"
  }

  # Mock rationale: The 'REQUIRED_TAGS' AWS Config rule expects input parameters
  # in the format of tag1Key, tag1Value, tag2Key, tag2Value, etc. This dynamic
  # generation ensures the correct format based on the 'required_tags' map.
  # For offline testing, we verify the structure of this generated JSON.
  input_parameters = jsonencode(merge([for idx, key in keys(var.required_tags) : {
    "tag${idx + 1}Key"   = key
    "tag${idx + 1}Value" = var.required_tags[key]
  }]...))

  scope {
    # Mock rationale: For offline testing, we assume the resource types are correctly passed.
    # The actual validation of resource types happens when Terraform interacts with AWS.
    # Our test will check if the 'compliance_resource_types' attribute is present in the plan.
    compliance_resource_types = var.resource_types
  }

  tags = {
    "ManagedBy" = "ApocalypsAI"
    "Utility"   = "nightly-tag-enforcer-watchdog"
  }
}

output "config_rule_arn" {
  description = "The ARN of the created AWS Config Rule."
  value       = aws_config_config_rule.required_tags_rule.arn
}
