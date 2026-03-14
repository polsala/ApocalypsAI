output \"bucket_arn\" {\n  description = \"ARN of the created bucket.\"\n  value       = aws_s3_bucket.this.arn\n}\n
