module "temporal_echo_chamber_test" {
  source = "../src"

  aws_region       = var.aws_region
  ami_id           = var.ami_id
  instance_type    = var.instance_type
  duration_minutes = var.duration_minutes
  tags = {
    Environment = "Test"
    Project     = "ApocalypsAI-EchoChamber"
  }
}

variable "aws_region" {
  description = "AWS region for testing."
  type        = string
  default     = "us-east-1"
}

variable "ami_id" {
  description = "Dummy AMI ID for testing."
  type        = string
  default     = "ami-0abcdef1234567890" # Mock rationale: A placeholder AMI ID for terraform plan validation. This ID is not expected to exist or be valid for actual provisioning, but allows `terraform plan` to proceed without error for syntax checks.
}

variable "instance_type" {
  description = "Instance type for testing."
  type        = string
  default     = "t2.micro"
}

variable "duration_minutes" {
  description = "Duration for testing."
  type        = number
  default     = 5
}
