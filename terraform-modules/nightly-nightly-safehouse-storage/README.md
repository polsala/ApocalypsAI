# Safehouse Storage Terraform Module

Creates a whimsical “safehouse” storage directory on the local filesystem. The directory name is a random pet name (e.g., "fluffy-otter"). Inside, a placeholder file `version.txt` is written with the version number you specify. Useful for local development, demos, or as a metaphorical vault for post‑apocalyptic data.

## Usage

```hcl
module "safehouse" {
  source  = "git::https://github.com/yourorg/ApocalypsAI.git//terraform-modules/nightly-safehouse-storage"
  version = "1"
}
```

Outputs:

- `safehouse_name` – the generated pet name.
- `safehouse_path` – absolute path to the created directory.

## Requirements

- Terraform ≥ 1.0
- No cloud provider needed; works entirely locally.

## Testing

```bash
cd terraform-modules/nightly-safehouse-storage
bash tests/test_module.sh
```
