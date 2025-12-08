variable "project_name" {
  description = "A unique name for the project, used for resource naming."
  type        = string
  default     = "morale-beacon"
}

variable "aws_region" {
  description = "The AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}

variable "uplifting_messages" {
  description = "A list of strings, each an uplifting message."
  type        = list(string)
  default     = [
    "Stay strong, survivor!",
    "Hope endures even in the darkest times.",
    "Together, we will rebuild!",
    "The dawn always follows the longest night.",
    "Your resilience is your greatest weapon."
  ]
}
