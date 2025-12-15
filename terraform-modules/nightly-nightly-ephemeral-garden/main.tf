resource "aws_instance" "garden_instance" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnet_id
  vpc_security_group_ids = var.vpc_security_group_ids
  associate_public_ip_address = var.associate_public_ip_address

  # Ephemeral characteristics
  disable_api_termination = false # Allow easy termination
  instance_initiated_shutdown_behavior = "terminate" # Ensure termination on shutdown

  tags = {
    Name        = "${var.name_prefix}-EphemeralGarden-EC2"
    Environment = "Ephemeral"
    ManagedBy   = "ApocalypsAI"
  }
}

resource "aws_s3_bucket" "garden_bucket" {
  bucket = "${var.name_prefix}-ephemeral-garden-bucket-${random_id.bucket_suffix.hex}"
  acl    = "private"

  # Ephemeral characteristics
  lifecycle_rule {
    id      = "expire_old_objects"
    enabled = true
    expiration {
      days = var.s3_object_expiration_days
    }
  }

  versioning {
    enabled = false # No versioning by default for ephemerality
  }

  tags = {
    Name        = "${var.name_prefix}-EphemeralGarden-S3"
    Environment = "Ephemeral"
    ManagedBy   = "ApocalypsAI"
  }
}

resource "aws_db_instance" "garden_db" {
  allocated_storage    = var.db_allocated_storage
  engine               = var.db_engine
  engine_version       = var.db_engine_version
  instance_class       = var.db_instance_class
  name                 = var.db_name
  username             = var.db_username
  password             = var.db_password
  vpc_security_group_ids = var.vpc_security_group_ids
  db_subnet_group_name = var.db_subnet_group_name
  publicly_accessible  = false

  # Ephemeral characteristics
  skip_final_snapshot = true # Don't take a final snapshot on deletion
  deletion_protection = false # Allow easy deletion

  tags = {
    Name        = "${var.name_prefix}-EphemeralGarden-RDS"
    Environment = "Ephemeral"
    ManagedBy   = "ApocalypsAI"
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}
