# Example: Basic Chaos Garden Setup

# Configure AWS provider
provider "aws" {
  region = "us-east-1"
}

# Create a VPC for our chaos garden
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "chaos-garden-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = false
  
  tags = {
    Environment = "chaos-demo"
    Purpose     = "chaos-garden"
  }
}

# Create security groups
resource "aws_security_group" "chaos_sg" {
  name        = "chaos-garden-sg"
  description = "Security group for chaos garden tasks"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
  
  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name        = "chaos-garden-sg"
    Environment = "chaos-demo"
  }
}

# Use the chaos garden module
module "chaos_garden" {
  source = "../../"
  
  # Basic configuration
  environment = "chaos-demo"
  chaos_duration = "15m"
  
  # Chaos scenarios
  enable_network_chaos = true
  network_latency_ms = 100
  enable_cpu_chaos = true
  cpu_stress_duration = "5m"
  enable_random_failures = true
  failure_rate = 0.05
  
  # Whimsical settings
  whimsy_level = "medium"
  chaos_garden_name = "ThePlayfulPandemonium"
  
  # ECS configuration
  task_cpu = 512
  task_memory = 1024
  chaos_task_count = 1
  
  # Networking
  subnet_ids          = module.vpc.private_subnets
  security_group_ids  = [aws_security_group.chaos_sg.id]
  
  # Logging
  log_retention_days = 1
  
  # Schedule (every 30 minutes for demo)
  chaos_schedule_expression = "rate(30 minutes)"
  
  # Tags
  additional_tags = {
    Demo = "true"
    Owner = "ApocalypsAI"
  }
}

# Output useful information
output "chaos_garden_info" {
  description = "Information about the deployed chaos garden"
  value = {
    cluster_id = module.chaos_garden.chaos_cluster_id
    service_name = module.chaos_garden.chaos_service_name
    task_definition = module.chaos_garden.chaos_task_definition
    log_group = module.chaos_garden.chaos_log_group
    notifications_topic = module.chaos_garden.chaos_notifications_topic
  }
}

output "chaos_configuration" {
  description = "Chaos configuration summary"
  value = module.chaos_garden.chaos_configuration
}
