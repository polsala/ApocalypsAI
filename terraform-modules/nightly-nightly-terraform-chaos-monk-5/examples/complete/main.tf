# Complete example of Chaos Monkey usage

# Example infrastructure to test
resource "aws_instance" "test_server" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  
  tags = {
    Name = "test-server"
  }
}

resource "aws_security_group" "test_sg" {
  name        = "test-security-group"
  description = "Test security group"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_rds_instance" "test_db" {
  identifier = "test-database"
  engine     = "postgres"
  instance_class = "db.t3.micro"
  allocated_storage = 20
  username = "admin"
  password = "password123"
  skip_final_snapshot = true
}

# Chaos Monkey module configuration
module "chaos_monkey" {
  source = "../.."
  
  # Enable chaos mode
  chaos_enabled = true
  
  # Moderate chaos probability
  chaos_probability = 0.15
  
  # Run chaos every 6 hours
  chaos_schedule = "0 */6 * * *"
  
  # Target specific resource types
  target_resource_types = [
    "aws_instance",
    "aws_security_group",
    "aws_rds_instance"
  ]
  
  # Exclude critical resources
  excluded_resources = [
    "production-db",
    "critical-load-balancer"
  ]
  
  # Start with dry-run mode for safety
  dry_run = true
  
  # Set log level to INFO
  log_level = "INFO"
}

# Output chaos metrics
output "chaos_metrics" {
  value = module.chaos_monkey.chaos_metrics
}

# Output safety warnings
output "safety_warnings" {
  value = module.chaos_monkey.safety_warnings
}

# Example of how to monitor chaos execution
resource "null_resource" "chaos_monitor" {
  triggers = {
    metrics = jsonencode(module.chaos_monkey.chaos_metrics)
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      echo "[MONITOR] Chaos metrics updated:"
      echo "${self.triggers.metrics}"
      
      # In a real implementation, you'd send this to your monitoring system
      # curl -X POST -H "Content-Type: application/json" \
      #   -d '${self.triggers.metrics}' \
      #   https://your-monitoring-system.com/metrics
    EOT
  }
}
