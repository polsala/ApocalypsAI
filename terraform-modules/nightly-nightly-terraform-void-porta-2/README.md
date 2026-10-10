# Void Portal Terraform Module

This module creates a playful “Void Portal” using Terraform's `null_resource` and the `random` provider. It generates a unique portal ID and can output a custom greeting.

## Features
- Generates a random 8‑byte hexadecimal portal ID.
- Optionally prints a custom greeting during apply.
- No real cloud resources are created – safe to run locally.

## Usage
```hcl
module "void_portal" {
  source       = "./"
  portal_name  = "My Secret Portal"
  greeting     = "Welcome, traveler!"
}
```

## Variables
| Name | Description | Type | Default |
|------|-------------|------|---------|
| `portal_name` | Human‑readable name for the portal | `string` | `"Void Portal"` |
| `greeting`    | Optional greeting printed on apply | `string` | `null` |

## Outputs
| Name | Description |
|------|-------------|
| `portal_id`        | Randomly generated portal identifier |
| `greeting_message`| The greeting that was printed (if any) |

## Testing
A simple validation script is provided under `tests/validate.sh`. Run it with:
```bash
cd <module‑directory>
./tests/validate.sh
```
The script runs `terraform init`, `terraform validate`, and a dry‑run `terraform plan` to ensure the module is syntactically correct.

## License
MIT – feel free to adapt the portal to your own apocalyptic needs!
