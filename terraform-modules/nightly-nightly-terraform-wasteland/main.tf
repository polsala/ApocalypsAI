#############################################
# Nightly Terraform Wasteland Terraform Module
# Post-apocalyptic infrastructure generator
#############################################

# Survival Resource Naming Convention
locals {
  survival_prefix = "wasteland"
  resource_suffix = format("-%s", var.environment)
  
  # Generate survival-themed names
  water_tank_names = [for i in range(var.water_tanks) : "${local.survival_prefix}-water-tank-${i + 1}${local.resource_suffix}"]
  food_store_names = [for i in range(var.food_stores) : "${local.survival_prefix}-food-store-${i + 1}${local.resource_suffix}"]
  power_gen_names = [for i in range(var.power_generators) : "${local.survival_prefix}-power-gen-${i + 1}${local.resource_suffix}"]
  watch_tower_names = var.perimeter_fencing ? [for i in range(var.watch_towers) : "${local.survival_prefix}-watch-tower-${i + 1}${local.resource_suffix}"] : []
  radio_tower_names = [for i in range(var.radio_towers) : "${local.survival_prefix}-radio-tower-${i + 1}${local.resource_suffix}"]
}

#############################################
# Survival Infrastructure Resources
#############################################

# Water Storage Infrastructure
resource "aws_s3_bucket" "water_tanks" {
  count = var.water_tanks
  
  bucket = local.water_tank_names[count.index]
  
  tags = {
    Name = "Water Storage Tank ${count.index + 1}"
    Environment = var.environment
    Type = "Survival-Resource"
    Resource = "Water-Storage"
    CreatedBy = "Terraform-Wasteland-Module"
  }
  
  lifecycle_rule {
    enabled = true
    
    expiration {
      days = 3650  # Keep water data for 10 years
    }
  }
}

# Food Storage Infrastructure
resource "aws_dynamodb_table" "food_stores" {
  count = var.food_stores
  
  name = local.food_store_names[count.index]
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "item_id"
  
  attribute {
    name = "item_id"
    type = "S"
  }
  
  tags = {
    Name = "Food Storage Facility ${count.index + 1}"
    Environment = var.environment
    Type = "Survival-Resource"
    Resource = "Food-Storage"
    CreatedBy = "Terraform-Wasteland-Module"
  }
}

# Power Generation Infrastructure
resource "aws_ec2_instance" "power_generators" {
  count = var.power_generators
  
  ami = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  
  tags = {
    Name = "Backup Power Generator ${count.index + 1}"
    Environment = var.environment
    Type = "Survival-Resource"
    Resource = "Power-Generation"
    CreatedBy = "Terraform-Wasteland-Module"
  }
  
  user_data = <<-EOF
              #!/bin/bash
              echo "Power generator ${count.index + 1} online"
              echo "Status: Operational"
              echo "Fuel: ${var.power_generators * 100} hours remaining"
              EOF
}

# Security Infrastructure
resource "aws_security_group" "perimeter_fencing" {
  count = var.perimeter_fencing ? 1 : 0
  
  name        = "${local.survival_prefix}-perimeter-fencing${local.resource_suffix}"
  description = "Perimeter security for survival compound"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Authorized access only"
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound"
  }
  
  tags = {
    Name = "Perimeter Security Fence"
    Environment = var.environment
    Type = "Security"
    Resource = "Perimeter-Fencing"
    CreatedBy = "Terraform-Wasteland-Module"
  }
}

# Watch Towers
resource "aws_ec2_instance" "watch_towers" {
  count = var.watch_towers
  
  ami = data.aws_ami.ubuntu.id
  instance_type = "t3.nano"
  
  tags = {
    Name = "Security Watch Tower ${count.index + 1}"
    Environment = var.environment
    Type = "Security"
    Resource = "Watch-Tower"
    CreatedBy = "Terraform-Wasteland-Module"
  }
  
  user_data = <<-EOF
              #!/bin/bash
              echo "Watch tower ${count.index + 1} active"
              echo "Surveillance: Active"
              echo "Threats detected: 0"
              EOF
}

# Communication Infrastructure
resource "aws_sns_topic" "radio_towers" {
  count = var.radio_towers
  
  name = local.radio_tower_names[count.index]
  
  tags = {
    Name = "Emergency Radio Tower ${count.index + 1}"
    Environment = var.environment
    Type = "Communication"
    Resource = "Radio-Tower"
    CreatedBy = "Terraform-Wasteland-Module"
    Frequency = var.emergency_frequency
  }
}

# Emergency Broadcast System
resource "aws_sns_topic_subscription" "emergency_broadcast" {
  count = var.radio_towers
  
  topic_arn = aws_sns_topic.radio_towers[count.index].arn
  protocol  = "email"
  endpoint  = "survivor@wasteland.com"
}

#############################################
# Data Sources
#############################################

data "aws_ami" "ubuntu" {
  most_recent = true
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
  
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  
  owners = ["099720109477"] # Canonical
}

#############################################
# Survival Metrics
#############################################

# Calculate survival readiness score
locals {
  water_capacity = var.water_tanks * 1000  # 1000 units per tank
  food_capacity = var.food_stores * 500    # 500 units per store
  power_capacity = var.power_generators * 24  # 24 hours per generator
  security_level = var.perimeter_fencing ? var.watch_towers * 10 : 0
  communication_range = var.radio_towers * 50  # 50 miles per tower
  
  total_survival_score = local.water_capacity + local.food_capacity + local.power_capacity + local.security_level + local.communication_range
}

#############################################
# Outputs
#############################################

output "survival_resources" {
  description = "Details of created survival infrastructure"
  value = {
    water_tanks = {
      count = var.water_tanks
      names = local.water_tank_names
      capacity = local.water_capacity
    }
    food_stores = {
      count = var.food_stores
      names = local.food_store_names
      capacity = local.food_capacity
    }
    power_generators = {
      count = var.power_generators
      names = local.power_gen_names
      capacity = local.power_capacity
    }
  }
}

output "security_perimeter" {
  description = "Security infrastructure details"
  value = {
    perimeter_fencing = var.perimeter_fencing
    watch_towers = {
      count = var.watch_towers
      names = local.watch_tower_names
      security_level = local.security_level
    }
    security_group_id = var.perimeter_fencing ? aws_security_group.perimeter_fencing[0].id : null
  }
}

output "communication_nodes" {
  description = "Communication infrastructure details"
  value = {
    radio_towers = {
      count = var.radio_towers
      names = local.radio_tower_names
      frequency = var.emergency_frequency
      range = local.communication_range
    }
    emergency_broadcast = var.radio_towers > 0 ? aws_sns_topic_subscription.emergency_broadcast : []
  }
}

output "total_survival_score" {
  description = "Overall survival readiness score (higher is better)"
  value = local.total_survival_score
  
  # Survival score interpretation
  # 0-1000: Critical - Immediate danger
  # 1001-5000: Poor - Basic survival
  # 5001-10000: Good - Sustainable
  # 10001+: Excellent - Thriving
}

output "survival_status" {
  description = "Human-readable survival status"
  value = local.total_survival_score >= 10001 ? "EXCELLENT - Thriving colony" :
           local.total_survival_score >= 5001 ? "GOOD - Sustainable survival" :
           local.total_survival_score >= 1001 ? "POOR - Basic survival" :
           "CRITICAL - Immediate danger"
}
