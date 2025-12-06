variable "region" {
  description = "AWS region to deploy"
  default = "us-west-2"
}

variable "azs" {
  description = "Availability zones for subnets"
  default = ["us-west-2a", "us-west-2b"]
}

variable "ssh_access_ip" {
  description = "IP address allowed SSH access"
  default = "0.0.0.0/0"
}

variable "instance_type" {
  description = "EC2 instance type for web servers"
  default = "t3.micro"
}
