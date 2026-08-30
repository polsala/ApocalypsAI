## Nightly Terraform Cloud-Init Generator

This Terraform module generates `cloud-init` user data for provisioning virtual machines with a whimsical yet functional security setup. It includes a randomized MOTD, a 'secret' handshake command, and a basic firewall configuration.

### Features

*   **Randomized MOTD**: A fun, ever-changing message of the day.
*   **Secret Handshake**: A simple command that must be run to unlock a 'hidden' message.
*   **Basic Firewall**: Configures `ufw` to allow SSH and a random port.
*   **User Management**: Creates a user with a randomized password.

### Usage

```hcl
module "cloud_init_server" {
  source = "./modules/nightly-terraform-cloud-init-gen"

  instance_name = "apocalypse-server-01"
  ssh_port      = 22
  secret_port   = 1337 # Example secret port
  admin_user    = "survivor"
  admin_password = "supersecretpassword"
}

resource "aws_instance" "example" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t2.micro"

  user_data = module.cloud_init_server.user_data

  tags = {
    Name = "${var.instance_name}"
  }
}
```

### Inputs

*   `instance_name` (string): The name of the instance.
*   `ssh_port` (number): The SSH port to open.
*   `secret_port` (number): A whimsical port for a secret command.
*   `admin_user` (string): The username for the admin user.
*   `admin_password` (string): The password for the admin user.
