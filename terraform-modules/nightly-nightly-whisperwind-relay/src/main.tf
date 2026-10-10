resource "aws_sqs_queue" "whisperwind_relay" {
  name                       = var.relay_name
  visibility_timeout_seconds = var.visibility_timeout_seconds
  message_retention_seconds  = var.message_retention_seconds
  delay_seconds              = var.delay_seconds

  tags = {
    ApocalypsAI = "WhisperwindRelay"
    Purpose     = "InterSettlementComms"
    ManagedBy   = "NightlyIntegrator"
  }
}
