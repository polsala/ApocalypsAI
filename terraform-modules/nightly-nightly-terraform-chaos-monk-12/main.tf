terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}

# Variables
variable "chaos_enabled" {
  description = "Enable/disable chaos engineering"
  type        = bool
  default     = false
}

variable "chaos_interval_hours" {
  description = "Hours between chaos runs"
  type        = number
  default     = 1
}

variable "max_resources_per_run" {
  description = "Maximum resources to terminate per run"
  type        = number
  default     = 1
}

variable "target_resource_types" {
  description = "Resource types to target for chaos"
  type        = list(string)
  default     = []
}

variable "excluded_resources" {
  description = "Resource names to exclude from chaos"
  type        = list(string)
  default     = []
}

variable "dry_run" {
  description = "Only log what would be destroyed, don't actually destroy"
  type        = bool
  default     = true
}

variable "aws_region" {
  description = "AWS region for chaos operations"
  type        = string
  default     = "us-east-1"
}

# Data sources to discover resources
locals {
  chaos_enabled = var.chaos_enabled && (var.target_resource_types != [] || var.excluded_resources != [])
  
  # Get current timestamp for chaos scheduling
  chaos_timestamp = formatdate("YYYY-MM-DDTHH:mm:ssZ", timestamp())
}

# Random number generator for chaos selection
resource "random_integer" "chaos_selector" {
  count  = local.chaos_enabled ? 1 : 0
  min    = 1
  max    = 100
  result = random_shuffle.chaos_resources[count.index].result[0]
}

# Random resource selector
resource "random_shuffle" "chaos_resources" {
  count  = local.chaos_enabled ? 1 : 0
  input  = data.aws_instances.selected.ids
  result_count = var.max_resources_per_run
}

# Discover EC2 instances for chaos
data "aws_instances" "selected" {
  count  = local.chaos_enabled ? 1 : 0
  
  filter {
    name   = "instance-state-name"
    values = ["running"]
  }
  
  filter {
    name   = "tag:Environment"
    values = ["test", "staging", "chaos"]
  }
  
  # Exclude critical resources
  for_each = { for id, name in var.excluded_resources : id => name }
}

# Chaos execution logic
resource "null_resource" "chaos_execution" {
  count  = local.chaos_enabled ? 1 : 0
  
  triggers = {
    chaos_run_id    = random_integer.chaos_selector[0].result
    chaos_timestamp = local.chaos_timestamp
    dry_run         = var.dry_run
  }
  
  provisioner "local-exec" {
    when    = destroy
    command = <<-EOT
      #!/bin/bash
      echo "=== CHAOS MONKEY EXECUTION ===" >> chaos_log.txt
      echo "Timestamp: ${local.chaos_timestamp}" >> chaos_log.txt
      echo "Dry Run: ${var.dry_run}" >> chaos_log.txt
      echo "Resources to terminate: ${join(", ", random_shuffle.chaos_resources[0].result)}" >> chaos_log.txt
      
      if [ "${var.dry_run}" = "false" ]; then
        echo "EXECUTING CHAOS - TERMINATING INSTANCES" >> chaos_log.txt
        for instance_id in ${join(" ", random_shuffle.chaos_resources[0].result)}; do
          aws ec2 terminate-instances --instance-ids $instance_id --region ${var.aws_region}
          echo "Terminated instance: $instance_id" >> chaos_log.txt
        done
      else
        echo "DRY RUN - Would have terminated: ${join(", ", random_shuffle.chaos_resources[0].result)}" >> chaos_log.txt
      fi
      
      echo "=== CHAOS EXECUTION COMPLETE ===" >> chaos_log.txt
    EOT
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      #!/bin/bash
      echo "CHAOS MONKEY SCHEDULED FOR NEXT RUN IN ${var.chaos_interval_hours} HOURS" >> chaos_schedule.txt
      echo "Next execution: $(date -d '+${var.chaos_interval_hours} hours' --iso-8601=seconds)" >> chaos_schedule.txt
    EOT
  }
}

# CloudWatch log group for chaos events
resource "aws_cloudwatch_log_group" "chaos_logs" {
  count       = local.chaos_enabled ? 1 : 0
  name        = "/aws/chaos-monkey/${terraform.workspace}"
  retention_in_days = 30
  
  tags = {
    Environment = terraform.workspace
    Purpose     = "chaos-engineering"
    CreatedBy   = "terraform-chaos-monkey"
  }
}

# IAM policy for chaos operations
resource "aws_iam_policy" "chaos_policy" {
  count  = local.chaos_enabled ? 1 : 0
  name   = "chaos-monkey-policy-${terraform.workspace}"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "ec2:DescribeInstances",
          "ec2:TerminateInstances",
          "ec2:DescribeTags"
        ],
        Resource = "*"
      },
      {
        Effect   = "Allow",
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:${var.aws_region}:*:log-group:/aws/chaos-monkey:*"
      }
    ]
  })
}

# Output chaos configuration
output "chaos_status" {
  value       = local.chaos_enabled
  description = "Whether chaos engineering is enabled"
}

output "chaos_log_group" {
  value       = aws_cloudwatch_log_group.chaos_logs[0].name
  description = "CloudWatch log group for chaos events"
  sensitive   = false
}

output "chaos_schedule" {
  value       = "Next chaos run in ${var.chaos_interval_hours} hours"
  description = "Scheduled chaos execution timing"
}
