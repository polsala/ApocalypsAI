resource "aws_s3_bucket" "echo_vault" {
  bucket_prefix = var.bucket_name_prefix
  acl           = "private" # Ensure private access by default

  tags = {
    ManagedBy   = "ApocalypsAI-NightlyIntegrator"
    UtilityName = "nightly-ephemeral-echo-vault"
    Ephemeral   = "true"
    DecayPeriod = "${var.decay_period_days}d"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "echo_vault_lifecycle" {
  bucket = aws_s3_bucket.echo_vault.id

  rule {
    id     = "temporal-decay-rule"
    status = "Enabled"

    expiration {
      days = var.decay_period_days
    }
  }
}
