# Example: Production-Safe Chaos Monkey Configuration

provider "aws" {
  region = "us-east-1"
}

module "chaos_monkey" {
  source = "../.."
  
  # Production-safe configuration
  prefix           = "prod-chaos"
  chaos_schedule   = "cron(0 3 * * ? *)"  # 3 AM UTC daily
  resource_types   = ["ec2", "rds", "elasticache"]
  max_chaos_per_run = 1
  dry_run          = false  # Real chaos
  enabled          = var.enable_chaos_engineering
  
  # Strict exclusion rules for production
  exclude_tags = {
    Environment = "production"
    Critical    = "true"
    Team        = "platform"
    Backup      = "daily"
  }
  
  # Enable notifications
  enable_notifications = true
  notification_email   = "platform-team@example.com"
  
  # Extended log retention
  log_retention_days = 30
  
  # Create monitoring dashboard
  create_dashboard = true
}

# Example of using a variable to control chaos engineering
variable "enable_chaos_engineering" {
  description = "Enable chaos engineering in production"
  type        = bool
  default     = false
  
  validation {
    condition     = var.enable_chaos_engineering == true || var.enable_chaos_engineering == false
    error_message = "enable_chaos_engineering must be true or false."
  }
}

# Example resources that would be protected
resource "aws_instance" "production_web_server" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t3.medium"
  
  tags = {
    Name        = "prod-web-server"
    Environment = "production"
    Team        = "platform"
  }
}

resource "aws_db_instance" "production_database" {
  identifier = "prod-database"
  
  engine         = "postgres"
  instance_class = "db.t3.micro"
  allocated_storage = 20
  
  tags = {
    Name        = "prod-database"
    Environment = "production"
    Critical    = "true"
    Backup      = "daily"
  }
}
