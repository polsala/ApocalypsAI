variable "name_prefix" {
  description = "A prefix for all resource names to ensure uniqueness and identification."
  type        = string
  default     = "apocalypsai"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance."
  type        = string
  default     = "ami-0abcdef1234567890" # Mock AMI for testing/example
}

variable "instance_type" {
  description = "The type of EC2 instance to launch."
  type        = string
  default     = "t3.micro"
}

variable "subnet_id" {
  description = "The ID of the subnet to launch the EC2 instance into."
  type        = string
  # Mock rationale: In a real scenario, this would be a valid subnet ID.
  # For offline testing, we provide a placeholder.
  default     = "subnet-0123456789abcdef0"
}

variable "vpc_security_group_ids" {
  description = "A list of security group IDs to associate with the EC2 instance and RDS database."
  type        = list(string)
  # Mock rationale: In a real scenario, these would be valid security group IDs.
  # For offline testing, we provide a placeholder.
  default     = ["sg-0abcdef1234567890"]
}

variable "associate_public_ip_address" {
  description = "Whether to associate a public IP address with the EC2 instance."
  type        = bool
  default     = false
}

variable "s3_object_expiration_days" {
  description = "Number of days after which S3 objects will expire."
  type        = number
  default     = 7
}

variable "db_allocated_storage" {
  description = "The allocated storage in gigabytes for the DB instance."
  type        = number
  default     = 20
}

variable "db_engine" {
  description = "The database engine to use."
  type        = string
  default     = "mysql"
}

variable "db_engine_version" {
  description = "The database engine version."
  type        = string
  default     = "5.7"
}

variable "db_instance_class" {
  description = "The instance type of the RDS database."
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "The name of the database to create."
  type        = string
  default     = "ephemeraldb"
}

variable "db_username" {
  description = "The master username for the database."
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "The master password for the database."
  type        = string
  default     = "Password123!" # In real use, use secrets management
  sensitive   = true
}

variable "db_subnet_group_name" {
  description = "The name of the DB subnet group to associate with the RDS instance."
  type        = string
  # Mock rationale: In a real scenario, this would be a valid DB subnet group name.
  # For offline testing, we provide a placeholder.
  default     = "default-vpc-0123456789abcdef0"
}
