variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}

variable "ami_id" {
  description = "The AMI ID for the EC2 instance (e.g., Ubuntu 22.04 LTS)."
  type        = string
  default     = "ami-053b0d53c279acc90" # Ubuntu Server 22.04 LTS (HVM), SSD Volume Type, us-east-1
}

variable "instance_type" {
  description = "The EC2 instance type."
  type        = string
  default     = "t2.micro"
}

variable "message_content" {
  description = "The message content to display on the web server."
  type        = string
  default     = "Greetings from the ApocalypsAI! This message will self-destruct."
}

variable "self_destruct_minutes" {
  description = "Number of minutes until the instance automatically shuts down."
  type        = number
  default     = 60 # 1 hour
}

variable "key_pair_name" {
  description = "Optional: The name of an existing EC2 Key Pair to allow SSH access."
  type        = string
  default     = "" # No key pair by default
}
