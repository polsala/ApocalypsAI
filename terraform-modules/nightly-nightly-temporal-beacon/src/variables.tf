variable "beacon_name" {
  description = "A unique name for the temporal beacon resources."
  type        = string
  default     = "temporal-beacon"
}

variable "schedule_expression" {
  description = "The CloudWatch Event Rule schedule expression (e.g., 'rate(1 hour)' or 'cron(0 12 * * ? *)')."
  type        = string
  default     = "rate(1 hour)"
}

variable "beacon_message" {
  description = "The message the beacon will emit to the log stream."
  type        = string
  default     = "Temporal Beacon: All systems nominal. Time continues."
}

variable "aws_region" {
  description = "The AWS region to deploy the beacon resources in."
  type        = string
  default     = "us-east-1"
}
