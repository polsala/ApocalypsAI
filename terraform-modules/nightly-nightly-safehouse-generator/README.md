# Nightly Safehouse Generator

A whimsical Terraform module that creates a local "safehouse" directory on your machine and writes a custom welcome message into a `message.txt` file. It uses the built‑in `null_resource` with a `local-exec` provisioner, so no external providers are required.

## Features

- No network access required – works entirely offline.
- Customizable welcome message via a Terraform variable.
- Simple to integrate into other Terraform configurations.

## Usage

```hcl
module "safehouse" {
  source          = "./path/to/nightly-safehouse-generator"
  welcome_message = "Welcome, survivor!"
}

output "safehouse_path" {
  value = module.safehouse.safehouse_path
}
```

Run the usual Terraform commands:

```bash
terraform init -backend=false -get=false
terraform apply -auto-approve -var='welcome_message=Hello from the bunker'
```

After apply, you will find a `safehouse` folder next to the module with a `message.txt` containing your message.

## Testing

The module includes an automated Bash test that validates the creation of the directory and the content of the message file. See `tests/test_main.sh`.
