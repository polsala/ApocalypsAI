resource "aws_secretsmanager_secret" "main" {
  name        = var.name
  description = var.description
  tags        = var.tags

  # Enable rotation if specified
  random_password_length = 16 # Default length if rotation is enabled but no specific length is provided
  random_password_include_numbers = true
  random_password_include_symbols = true
  random_password_include_uppercase = true
  random_password_include_lowercase = true

  # Apply resource policy if provided
  policy = var.resource_policy

  # Configure rotation if enabled
  dynamic "rotation" {
    for_each = var.rotation_enabled ? [1] : []
    content {
      rotation_lambda_arn = var.rotation_lambda_arn
      # You can add rotation_rules here if needed, e.g., schedule
      # rotation_rules {
      #   automatically_after_days = 30
      # }
    }
  }
}

resource "aws_secretsmanager_secret_version" "initial" {
  secret_id     = aws_secretsmanager_secret.main.id
  # Provide an initial placeholder secret value. In a real-world scenario, this might be generated or managed differently.
  secret_string = jsonencode({
    "placeholder" = "initial_value"
  })

  # Ensure the secret is created before creating the first version
  depends_on = [
    aws_secretsmanager_secret.main
  ]
}

variable "name" {
  description = "The name of the secret."
  type        = string
}

variable "description" {
  description = "A description of the secret."
  type        = string
  default     = null
}

variable "tags" {
  description = "A map of tags to assign to the secret."
  type        = map(string)
  default     = {}
}

variable "resource_policy" {
  description = "A JSON string representing the resource policy for the secret."
  type        = string
  default     = null
}

variable "rotation_enabled" {
  description = "Whether to enable secret rotation."
  type        = bool
  default     = false
}

variable "rotation_lambda_arn" {
  description = "The ARN of the Lambda function to use for rotation. Required if rotation_enabled is true."
  type        = string
  default     = null
}

output "secret_arn" {
  description = "The ARN of the created secret."
  value       = aws_secretsmanager_secret.main.arn
}

output "secret_name" {
  description = "The name of the created secret."
  value       = aws_secretsmanager_secret.main.name
}

output "secret_version_id" {
  description = "The ID of the latest version of the secret."
  value       = aws_secretsmanager_secret_version.initial.version_id
}
