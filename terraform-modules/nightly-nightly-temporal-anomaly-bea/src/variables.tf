variable "project_name" {
  description = "The name of the project, used for resource naming."
  type        = string
}

variable "environment" {
  description = "The deployment environment (e.g., dev, prod), used for resource naming."
  type        = string
}

variable "anomaly_pattern" {
  description = "The log pattern to search for in CloudWatch logs (e.g., 'Temporal Distortion Detected')."
  type        = string
}

variable "alarm_threshold" {
  description = "The number of anomalies within the period to trigger the alarm."
  type        = number
  default     = 1
}

variable "notification_email" {
  description = "Email address to subscribe to the SNS topic for alerts."
  type        = string
}

variable "aws_region" {
  description = "AWS region where resources will be deployed."
  type        = string
}
