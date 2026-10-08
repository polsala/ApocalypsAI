resource "aws_secretsmanager_secret" "ephemeral_secret" {
  name                    = var.secret_name
  description             = var.description
  recovery_window_in_days = var.recovery_window_in_days
  tags = {
    ManagedBy = "ApocalypsAI-NightlyIntegrator"
    Ephemeral = "true"
  }
}

resource "aws_secretsmanager_secret_version" "ephemeral_secret_version" {
  secret_id     = aws_secretsmanager_secret.ephemeral_secret.id
  secret_string = var.secret_string
}
