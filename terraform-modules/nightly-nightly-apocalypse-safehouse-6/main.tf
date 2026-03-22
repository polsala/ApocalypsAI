terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "supplies" {
  bucket = "${var.safehouse_name}-supplies"
  acl    = "private"
  tags = {
    Name = "${var.safehouse_name} Supplies"
  }
}

resource "aws_dynamodb_table" "inventory" {
  name         = "${var.safehouse_name}-inventory"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "item_id"

  attribute {
    name = "item_id"
    type = "S"
  }

  tags = {
    Name = "${var.safehouse_name} Inventory"
  }
}

resource "aws_iam_role" "safehouse_role" {
  name = "${var.safehouse_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "safehouse_policy" {
  name   = "${var.safehouse_name}-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:ListBucket"]
        Resource = [
          aws_s3_bucket.supplies.arn,
          "${aws_s3_bucket.supplies.arn}/*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["dynamodb:Query", "dynamodb:GetItem", "dynamodb:Scan"]
        Resource = [aws_dynamodb_table.inventory.arn]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.safehouse_role.name
  policy_arn = aws_iam_policy.safehouse_policy.arn
}
