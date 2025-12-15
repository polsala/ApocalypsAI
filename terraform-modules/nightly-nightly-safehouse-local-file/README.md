# Nightly Safehouse Local File Terraform Module

## Overview

This tiny Terraform module creates a **local file** that can serve as a mock "safehouse log" in a post‑apocalyptic scenario.  It is completely offline‑friendly – it uses only the built‑in `local` provider, so no cloud credentials are required.

## Features

- Generates a file at a user‑specified path.
- Allows custom content (e.g., a list of supplies, survivor names, or cryptic notes).
- Exposes the file path as an output for downstream modules.
- Includes a simple test script that runs `terraform init`, `validate` and `plan` without contacting any remote services.

## Usage

```hcl
module "safehouse_log" {
  source     = "./utils/nightly-safehouse-local-file"
  file_path  = "./safehouse.log"
  content    = <<EOT
Survivors: 12
Food rations: 42 days
Location: Sector 7G
EOT
}

output "log_path" {
  value = module.safehouse_log.file_path
}
```

## Variables

| Name | Type | Description | Default |
|------|------|-------------|---------|
| `file_path` | `string` | Path where the file will be created. | n/a |
| `content`   | `string` | Text content written to the file. | `"Safehouse initialized.\n"` |

## Outputs

| Name | Description |
|------|-------------|
| `file_path` | The absolute path of the generated file. |

## Testing

A minimal test script is provided under `tests/`. Run it with:

```bash
cd utils/nightly-safehouse-local-file
bash tests/test_module.sh
```

If everything is set up correctly you will see `Tests passed`.

## License

MIT – feel free to adapt, remix, and deploy your own safehouse utilities!
