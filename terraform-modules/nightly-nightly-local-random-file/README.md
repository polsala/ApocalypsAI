# nightly-local-random-file

## Overview

A tiny Terraform module that generates a random string (using the `random_id` resource) and writes it to a local file via the `local_file` resource.  It requires **no cloud provider** and works entirely offline, making it perfect for quick sandbox experiments or CI checks.

## Features

- Configurable output filename
- Configurable length of the random string (in bytes, then hex‑encoded)
- Outputs the generated string for downstream use

## Usage

```hcl
module "random_file" {
  source   = "./utils/nightly-local-random-file"
  filename = "example.txt"
  length   = 8
}

output "generated_string" {
  value = module.random_file.random_string
}
```

Run the usual Terraform commands:

```bash
terraform init -backend=false
terraform apply -auto-approve -var='filename=example.txt' -var='length=8'
```

The file `example.txt` will be created in the working directory containing a random 8‑byte (16‑character hex) string.

## Testing

The test suite is a simple Bash script that runs `terraform init` and `terraform validate` against the module with example variables.  It asserts that both commands exit with status `0`.

```bash
cd utils/nightly-local-random-file
bash tests/test_main.sh
```

## License

MIT © ApocalypsAI
