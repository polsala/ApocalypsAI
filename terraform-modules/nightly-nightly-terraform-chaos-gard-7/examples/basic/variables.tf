# AWS Region for the example
variable "aws_region" {
  description = "AWS region for the chaos garden demo"
  type        = string
  default     = "us-east-1"
}

# Environment name
variable "environment" {
  description = "Environment name for tagging"
  type        = string
  default     = "chaos-demo"
}

# Chaos settings
variable "chaos_duration" {
  description = "How long chaos runs"
  type        = string
  default     = "15m"
}

variable "enable_network_chaos" {
  description = "Enable network latency chaos"
  type        = bool
  default     = true
}

variable "network_latency_ms" {
  description = "Network latency in milliseconds"
  type        = number
  default     = 100
}

variable "enable_cpu_chaos" {
  description = "Enable CPU stress chaos"
  type        = bool
  default     = true
}

variable "cpu_stress_duration" {
  description = "CPU stress duration"
  type        = string
  default     = "5m"
}

variable "enable_random_failures" {
  description = "Enable random task failures"
  type        = bool
  default     = true
}

variable "failure_rate" {
  description = "Probability of random failures"
  type        = number
  default     = 0.05
}

# Whimsy settings
variable "whimsy_level" {
  description = "Whimsy level"
  type        = string
  default     = "medium"
}

variable "chaos_garden_name" {
  description = "Name for your chaos garden"
  type        = string
  default     = "ThePlayfulPandemonium"
}

# ECS settings
variable "task_cpu" {
  description = "CPU units for the ECS task"
  type        = number
  default     = 512
}

variable "task_memory" {
  description = "Memory for the ECS task (in MiB)"
  type        = number
  default     = 1024
}

variable "chaos_task_count" {
  description = "Number of chaos tasks to run"
  type        = number
  default     = 1
}

# Schedule
variable "chaos_schedule_expression" {
  description = "CloudWatch Events schedule expression"
  type        = string
  default     = "rate(30 minutes)"
}

# Logging
variable "log_retention_days" {
  description = "Number of days to retain logs"
  type        = number
  default     = 1
}

# Additional tags
variable "additional_tags" {
  description = "Additional tags to apply"
  type        = map(string)
  default     = {
    Demo  = "true"
    Owner = "ApocalypsAI"
  }
}
