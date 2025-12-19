# Complete Example: Terraform Chaos Monkey

# Configure providers
provider "aws" {
  region = "us-east-1"
}

provider "google" {
  project = var.gcp_project
  region  = "us-central1"
}

provider "azurerm" {
  features {}
}

# Chaos Monkey Module
module "chaos_monkey" {
  source = "./../"
  
  # Enable chaos engineering
  chaos_enabled = true
  
  # Configure chaos intervals (in minutes)
  chaos_interval = 30
  
  # Resource types to target
  target_resource_types = [
    "aws_instance",
    "aws_rds_instance",
    "aws_lambda_function"
  ]
  
  # Safety mechanisms
  protected_resources = [
    "production-db",
    "critical-api",
    "chaos-monkey-",
    "terraform-"
  ]
  
  # Maximum resources to terminate per cycle
  max_destructions_per_cycle = 3
  
  # Chaos schedule (cron format) - Every 4 hours
  chaos_schedule = "0 */4 * * *"
  
  # Enable dry run mode for testing
  dry_run = false
  
  # AWS region for Lambda
  aws_region = "us-east-1"
}

# Example AWS Resources (for testing)
resource "aws_instance" "test_instance_1" {
  ami           = "ami-0c02fb55956c7d316" # Amazon Linux 2 in us-east-1
  instance_type = "t2.micro"
  
  tags = {
    Name = "test-instance-1"
  }
}

resource "aws_instance" "test_instance_2" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"
  
  tags = {
    Name = "test-instance-2"
  }
}

resource "aws_db_instance" "test_db" {
  identifier = "test-db"
  
  engine         = "postgres"
  instance_class = "db.t3.micro"
  allocated_storage = 20
  
  name     = "testdb"
  username = "postgres"
  password = "password123"
  
  skip_final_snapshot = true
}

resource "aws_lambda_function" "test_function" {
  filename         = "${path.module}/lambda/test_function.zip"
  function_name    = "test-function"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "index.handler"
  source_code_hash = filebase64sha256("${path.module}/lambda/test_function.zip")
  runtime          = "python3.9"
  
  environment {
    variables = {
      TEST_VAR = "test_value"
    }
  }
}

# IAM Role for Lambda execution
resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Outputs
output "chaos_monkey_status" {
  description = "Chaos monkey configuration status"
  value       = {
    enabled           = module.chaos_monkey.chaos_enabled
    schedule          = module.chaos_monkey.chaos_schedule
    protected_count   = length(module.chaos_monkey.protected_resources)
    target_types      = module.chaos_monkey.target_resource_types
    max_destructions  = module.chaos_monkey.max_destructions_per_cycle
    dry_run           = module.chaos_monkey.dry_run_mode
  }
}

output "test_resources" {
  description = "Test resources created for chaos monkey"
  value       = {
    ec2_instances = [
      aws_instance.test_instance_1.id,
      aws_instance.test_instance_2.id
    ]
    rds_instance = aws_db_instance.test_db.id
    lambda_function = aws_lambda_function.test_function.arn
  }
}

# Variables
variable "gcp_project" {
  description = "GCP project ID"
  type        = string
  default     = ""
}

# Notes:
# - This example creates test resources that can be targeted by the chaos monkey
# - In a real environment, ensure proper IAM permissions and resource tagging
# - Always use dry run mode first to test your configuration
# - Monitor CloudWatch logs for chaos monkey activity
# - Consider using resource tagging for better chaos targeting
