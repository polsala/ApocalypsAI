## Nightly Terraform Cloud-Init Generator

This Terraform module generates a basic `cloud-init` configuration suitable for provisioning virtual machines in cloud environments. It includes a whimsical touch by adding a fun banner to the user data.

### Features

*   Generates `cloud-init` user data in `cloud-config` format.
*   Includes a customizable, whimsical banner.
*   Allows for the addition of arbitrary shell scripts.
*   Designed for easy integration into existing Terraform infrastructure.

### Usage

```hcl
module "cloud_init_server" {
  source = "./modules/nightly-tf-cloud-init-gen"

  instance_name = "my-whimsical-server"
  banner_message = "Welcome, brave explorer, to the digital frontier!"
  user_data_script = <<EOF
#!/bin/bash
echo "Hello from the custom script!"
apt-get update && apt-get install -y cowsay
cowsay "Moo!"
EOF
}
```

### Inputs

| Name               | Description                                                                 | Type    | Default                                                                 |
| ------------------ | --------------------------------------------------------------------------- | ------- | ----------------------------------------------------------------------- |
| `instance_name`    | A name for the instance, used in the whimsical banner.                      | `string`| `"ApocalypsAI Instance"`                                                |
| `banner_message`   | The core message for the whimsical banner.                                  | `string`| `"Greetings from the digital ether!"`                                 |
| `user_data_script` | A string containing a shell script to be executed by cloud-init.            | `string`| `null`                                                                  |
| `package_list`     | A list of packages to install via `apt-get`.                                | `list(string)` | `[]`                                                                    |

### Outputs

| Name           | Description                                                                 |
| -------------- | --------------------------------------------------------------------------- |
| `user_data`    | The generated `cloud-init` user data string.                                |
