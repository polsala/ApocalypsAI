# Complete Chaos Monkey Example

# Configure providers
provider "aws" {
  region = "us-east-1"
}

# Chaos Monkey Module
module "chaos_monkey" {
  source = "../.."
  
  # Enable chaos engineering
  chaos_enabled = true
  
  # Chaos configuration
  chaos_interval_hours = 2
  max_resources_per_run = 3
  
  # Resource types to target
  target_resource_types = [
    "aws_instance",
    "aws_rds_instance",
    "aws_elasticache_cluster"
  ]
  
  # Safety exclusions
  excluded_resources = [
    "production-db",
    "critical-app-server",
    "master-replica"
  ]
  
  # Dry run mode (set to false for actual chaos)
  dry_run = true
  
  # Environment filtering
  environment = "staging"
  
  # Advanced settings
  max_chaos_duration_minutes = 15
  chaos_schedule_cron = "0 2 * * *"
  enable_chaos_metrics = true
  chaos_retention_days = 90
  
  # Optional: SNS topic for notifications
  # chaos_notification_topic = "arn:aws:sns:us-east-1:123456789012:chaos-notifications"
}

# Example EC2 instances for chaos testing
resource "aws_instance" "chaos_test_1" {
  ami           = "ami-0c02fb55956c7d316" # Amazon Linux 2 in us-east-1
  instance_type = "t3.micro"
  
  tags = {
    Name        = "chaos-test-instance-1"
    Environment = "staging"
    Purpose     = "chaos-testing"
  }
}

resource "aws_instance" "chaos_test_2" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t3.micro"
  
  tags = {
    Name        = "chaos-test-instance-2"
    Environment = "staging"
    Purpose     = "chaos-testing"
  }
}

# Example RDS instance for chaos testing
resource "aws_db_instance" "chaos_test_db" {
  identifier = "chaos-test-db"
  
  engine         = "mysql"
  engine_version = "8.0.32"
  instance_class = "db.t3.micro"
  allocated_storage = 20
  
  username = "admin"
  password = "password123"
  
  skip_final_snapshot = true
  
  tags = {
    Name        = "chaos-test-db"
    Environment = "staging"
    Purpose     = "chaos-testing"
  }
}

# Example ElastiCache cluster for chaos testing
resource "aws_elasticache_cluster" "chaos_test_cache" {
  cluster_id           = "chaos-test-cache"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis6.x"
  
  tags = {
    Name        = "chaos-test-cache"
    Environment = "staging"
    Purpose     = "chaos-testing"
  }
}

# Output chaos configuration
output "chaos_configuration" {
  value = {
    enabled           = module.chaos_monkey.chaos_status
    log_group         = module.chaos_monkey.chaos_log_group
    schedule          = module.chaos_monkey.chaos_schedule
    dry_run           = var.dry_run
    target_resources  = var.target_resource_types
    excluded_resources = var.excluded_resources
  }
}
