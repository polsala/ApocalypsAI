variable "owner" {
  description = "Team/owner identifier for resource tagging"
  type = string
}

variable "environment" {
  description = "Environment context (prod/test/dev)"
  type = string
  default = "test"
}

variable "chaos_level" {
  description = "Chaos intensity level (1-5) for future expansion"
  type = number
  default = 2
}
