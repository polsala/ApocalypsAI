resource "aws_security_group" "anomaly_post_sg" {
  name        = "${var.tags["Name"] == "" ? "temporal-anomaly-post-sg" : "${var.tags["Name"]}-sg"}"
  description = "Allow SSH and HTTP access to Temporal Anomaly Observation Post"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow SSH from anywhere"
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow HTTP from anywhere"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = var.tags
}

resource "aws_instance" "anomaly_observer" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name == "" ? null : var.key_name
  vpc_security_group_ids = [aws_security_group.anomaly_post_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install -y nginx
              sudo systemctl start nginx
              sudo systemctl enable nginx
              
              # Whimsical Anomaly Detector Script
              echo "Temporal Anomaly Detector v1.0" > /var/www/html/index.html
              echo "<p>Scanning for temporal distortions...</p>" >> /var/www/html/index.html
              echo "<p>Last scan: $(date)</p>" >> /var/www/html/index.html
              
              # Simulate anomaly logging
              ANOMALY_LOG_FILE="/var/log/anomaly_log.txt"
              touch $ANOMALY_LOG_FILE
              echo "Anomaly detected at $(date) - Magnitude: $(shuf -i 1-100 -n 1)" >> $ANOMALY_LOG_FILE
              
              # Basic cron job to update anomaly status and log
              (crontab -l 2>/dev/null; echo "*/5 * * * * /bin/bash -c 'echo \"Temporal Anomaly Detector v1.0\" > /var/www/html/index.html; echo \"<p>Scanning for temporal distortions...</p>\" >> /var/www/html/index.html; echo \"<p>Last scan: $(date)\"</p>\" >> /var/www/html/index.html; echo \"Anomaly detected at $(date) - Magnitude: $(shuf -i 1-100 -n 1)\" >> /var/log/anomaly_log.txt'") | crontab -
              EOF

  tags = merge(var.tags, {
    Name = "${var.tags["Name"] == "" ? "Temporal-Anomaly-Observer" : var.tags["Name"]}"
  })
}

resource "aws_s3_bucket" "anomaly_log_vault" {
  bucket = "${var.tags["Name"] == "" ? "temporal-anomaly-log-vault-${random_id.bucket_suffix.hex}" : "${lower(replace(var.tags["Name"], " ", "-"))}-log-vault-${random_id.bucket_suffix.hex}"}"

  tags = merge(var.tags, {
    Name = "${var.tags["Name"] == "" ? "Temporal-Anomaly-Log-Vault" : "${var.tags["Name"]}-Log-Vault"}"
  })
}

resource "aws_s3_bucket_versioning" "anomaly_log_vault_versioning" {
  bucket = aws_s3_bucket.anomaly_log_vault.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "anomaly_log_vault_encryption" {
  bucket = aws_s3_bucket.anomaly_log_vault.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Data source to get the default VPC ID
data "aws_vpc" "default" {
  default = true
}

# Random ID for unique S3 bucket naming
resource "random_id" "bucket_suffix" {
  byte_length = 8
}
