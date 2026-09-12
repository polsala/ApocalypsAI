variable "resource_tags" {
  description = "A map of tags to identify resources to be hibernated (e.g., { 'Environment' = 'dev', 'Hibernatable' = 'true' })."
  type        = map(string)
  default     = {}
}

variable "stop_cron_schedule" {
  description = "The cron expression for when to stop resources (e.g., 'cron(0 22 * * ? *)' for 10 PM UTC daily)."
  type        = string
}

variable "start_cron_schedule" {
  description = "The cron expression for when to start resources (e.g., 'cron(0 8 * * ? *)' for 8 AM UTC daily)."
  type        = string
}

variable "region" {
  description = "The AWS region where resources are located and the scheduler will operate."
  type        = string
}

variable "name_prefix" {
  description = "A prefix for all created AWS resources to ensure uniqueness."
  type        = string
  default     = "hibernation-pod"
}
