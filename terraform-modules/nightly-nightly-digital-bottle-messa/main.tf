resource "aws_s3_bucket" "message_bottle" {
  bucket = "${var.project_name}-digital-message-bottle"
  acl    = "private" # Keep it private by default

  versioning {
    enabled = true # Keep history of messages
  }

  tags = {
    Project     = var.project_name
    Environment = "apocalypsai-utility"
    Utility     = "digital-message-bottle"
  }
}

resource "aws_dynamodb_table" "message_metadata" {
  name         = "${var.project_name}-MessageBottleMetadata"
  billing_mode = "PAY_PER_REQUEST" # Serverless, cost-effective

  hash_key = "MessageID"

  attribute {
    name = "MessageID"
    type = "S"
  }

  tags = {
    Project     = var.project_name
    Environment = "apocalypsai-utility"
    Utility     = "digital-message-bottle"
  }
}
