variable "region" {
  description = "The AWS region to deploy the beacons."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "The EC2 instance type for the beacons."
  type        = string
  default     = "t3.micro"
}

variable "ami_id" {
  description = "The AMI ID to use for the beacons. If null, a recent Amazon Linux 2 AMI will be selected."
  type        = string
  default     = null
}

variable "key_name" {
  description = "The name of the EC2 Key Pair to allow SSH access to the beacons (optional, but recommended for debugging)."
  type        = string
  default     = null
}

variable "beacon_count" {
  description = "The number of ephemeral beacons to deploy."
  type        = number
  default     = 1
}

variable "task_script" {
  description = "The bash script or command to execute on each beacon. This will be run after startup."
  type        = string
  default     = "echo 'No specific task defined. Beacon is just observing the void.'"
}

variable "self_terminate" {
  description = "If true, the beacon instances will attempt to terminate themselves after the task script completes."
  type        = bool
  default     = true
}

variable "log_bucket_name" {
  description = "Optional: The name of an S3 bucket to upload beacon logs to. If null, logs are only local."
  type        = string
  default     = null
}

variable "security_group_ids" {
  description = "A list of security group IDs to associate with the beacon instances. Required for network access."
  type        = list(string)
  default     = []
}
