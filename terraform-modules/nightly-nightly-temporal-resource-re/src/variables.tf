variable "source_instance_id" {
  description = "The ID of the existing EC2 instance to replicate."
  type        = string
}

variable "target_region" {
  description = "The AWS region where the replica instance will be created."
  type        = string
}

variable "replica_name_prefix" {
  description = "A prefix for the name tag of the replicated instance."
  type        = string
  default     = "echo"
}

variable "ami_override" {
  description = "Optional: Override the AMI ID of the source instance."
  type        = string
  default     = null
}

variable "instance_type_override" {
  description = "Optional: Override the instance type of the source instance."
  type        = string
  default     = null
}

variable "tags_to_add" {
  description = "Optional: A map of additional tags to apply to the replicated instance."
  type        = map(string)
  default     = {}
}

variable "subnet_id" {
  description = "Optional: The ID of the subnet to launch the instance into. If not provided, Terraform will attempt to use the default subnet in the target region."
  type        = string
  default     = null
}

variable "security_group_ids" {
  description = "Optional: A list of security group IDs to associate with the instance. If not provided, Terraform will attempt to use the default security group in the target region."
  type        = list(string)
  default     = []
}
