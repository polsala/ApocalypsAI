variable "region" {
  description = "The AWS region to deploy the beacon."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "The EC2 instance type for the beacon server."
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "The name of an existing EC2 Key Pair to allow SSH access to the beacon server. Leave empty if no SSH access is desired."
  type        = string
  default     = ""
}

variable "beacon_message" {
  description = "The message to be displayed on the Cloud Beacon's webpage."
  type        = string
  default     = "Seeking survivors. All systems nominal. Stay vigilant."
}
