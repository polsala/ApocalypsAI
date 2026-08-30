resource "aws_s3_bucket" "secret_vault" {
  bucket = var.bucket_name

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  lifecycle_rule {
    enabled = true
    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }

  tags = {
    Purpose = "Cryptic Keep"
  }
}

resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket = aws_s3_bucket.secret_vault.id

  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls  = true
  restrict_public_buckets = true
}

resource "aws_secretsmanager_secret" "vault_password" {
  name = "${var.bucket_name}-password"
  description = "Auto‑generated password for the cryptic keep"
}

resource "random_password" "generated" {
  length  = var.password_length
  special = true
}

resource "aws_secretsmanager_secret_version" "vault_password_version" {
  secret_id     = aws_secretsmanager_secret.vault_password.id
  secret_string = random_password.generated.result
}
