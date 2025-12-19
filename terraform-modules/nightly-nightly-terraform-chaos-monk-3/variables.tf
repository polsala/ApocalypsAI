# Chaos Engineering Configuration

variable "chaos_enabled" {
  description = "Enable or disable chaos engineering"
  type        = bool
  default     = false
}

variable "chaos_interval" {
  description = "Interval between chaos cycles in minutes"
  type        = number
  default     = 60
}

variable "target_resource_types" {
  description = "List of resource types to target for chaos"
  type        = list(string)
  default     = ["aws_instance", "aws_rds_instance"]
}

variable "protected_resources" {
  description = "List of resource names to protect from chaos"
  type        = list(string)
  default     = []
}

variable "max_destructions_per_cycle" {
  description = "Maximum number of resources to destroy per chaos cycle"
  type        = number
  default     = 1
}

variable "chaos_schedule" {
  description = "Cron schedule for chaos execution"
  type        = string
  default     = "0 */6 * * *" # Every 6 hours
}

variable "dry_run" {
  description = "Enable dry run mode (logs actions but doesn't execute them)"
  type        = bool
  default     = false
}

variable "aws_region" {
  description = "AWS region for Lambda function"
  type        = string
  default     = "us-east-1"
}

variable "gcp_project" {
  description = "GCP project ID for GCP resources"
  type        = string
  default     = ""
}

variable "azure_subscription_id" {
  description = "Azure subscription ID for Azure resources"
  type        = string
  default     = ""
}

# Outputs
output "chaos_enabled" {
  description = "Whether chaos engineering is enabled"
  value       = var.chaos_enabled
}

output "chaos_schedule" {
  description = "Cron schedule for chaos execution"
  value       = var.chaos_schedule
}

output "chaos_lambda_arn" {
  description = "ARN of the chaos monkey lambda function"
  value       = var.chaos_enabled ? aws_lambda_function.chaos_monkey[0].arn : ""
  sensitive   = true
}

output "protected_resources" {
  description = "Resources protected from chaos"
  value       = var.protected_resources
}

output "target_resource_types" {
  description = "Resource types targeted for chaos"
  value       = var.target_resource_types
}

output "max_destructions_per_cycle" {
  description = "Maximum destructions per chaos cycle"
  value       = var.max_destructions_per_cycle
}

output "dry_run_mode" {
  description = "Whether dry run mode is enabled"
  value       = var.dry_run
}
