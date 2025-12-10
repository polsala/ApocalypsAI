resource "aws_secretsmanager_secret" "vault" {
  name = var.vault_name
  tags = {
    "ManagedBy" = "ApocalypsAI"
    "Utility"   = "TerraVaultKeeper"
  }
}

resource "aws_secretsmanager_secret_version" "secrets" {
  for_each = var.secret_definitions

  secret_id     = aws_secretsmanager_secret.vault.id
  secret_string = jsonencode({
    # In a real-world scenario, you'd generate random strings here.
    # For this example, we're using the provided value.
    value = each.value.value
  })
}

# Basic rotation setup (conceptual - requires additional resources like Lambda, CloudWatch Events)
# This is a placeholder to illustrate the intent of rotation.
# A full implementation would involve creating a Lambda function to generate new secrets
# and a CloudWatch Event Rule to trigger it on the specified interval.

resource "aws_cloudwatch_event_rule" "rotation_schedule" {
  count = var.rotation_enabled ? 1 : 0
  name  = "${var.vault_name}-rotation-schedule"

  schedule_expression = var.rotation_interval
  is_enabled          = true

  tags = {
    "ManagedBy" = "ApocalypsAI"
    "Utility"   = "TerraVaultKeeper"
  }
}

# Placeholder for Lambda function that performs rotation
# resource "aws_lambda_function" "rotation_lambda" {
#   count = var.rotation_enabled ? 1 : 0
#   # ... lambda configuration ...
# }

# resource "aws_cloudwatch_event_target" "rotation_target" {
#   count = var.rotation_enabled ? 1 : 0
#   rule      = aws_cloudwatch_event_rule.rotation_schedule[0].name
#   target_id = "RotationLambda"
#   arn       = aws_lambda_function.rotation_lambda[0].arn
# }

output "vault_arn" {
  description = "The ARN of the provisioned cloud vault."
  value       = aws_secretsmanager_secret.vault.arn
}

output "secret_arns" {
  description = "A map of secret names to their respective ARNs."
  value       = { for name, secret in aws_secretsmanager_secret_version.secrets : name => secret.arn }
}
