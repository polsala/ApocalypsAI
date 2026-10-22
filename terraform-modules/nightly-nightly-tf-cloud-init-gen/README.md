# Terraform Cloud-Init Generator

This module generates Terraform HCL for cloud-init configurations, complete with whimsically named servers. It's designed to be a fun and functional way to bootstrap your cloud instances.

## Features

*   Generates `user_data` for cloud-init.
*   Assigns whimsical, apocalypse-themed names to servers.
*   Supports basic shell script execution on boot.

## Usage

```hcl
module "cloud_init_server" {
  source = "./path/to/nightly-tf-cloud-init-gen"

  server_name = "ScavengerBot-001"
  boot_script = "echo 'Welcome, survivor!' > /tmp/welcome.txt"
}

resource "aws_instance" "example" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t2.micro"
  user_data     = module.cloud_init_server.user_data

  tags = {
    Name = "My-Whimsical-Instance"
  }
}
```

## Inputs

*   `server_name` (string): The base name for the server. A whimsical suffix will be appended.
*   `boot_script` (string, optional): A shell script to execute on instance boot.

## Outputs

*   `user_data` (string): The generated cloud-init `user_data` content.
