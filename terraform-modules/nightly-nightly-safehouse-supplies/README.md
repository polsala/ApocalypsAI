# Safehouse Supplies Terraform Module

This module creates a local directory representing a safe‑house and writes a text file for each listed supply. It is useful for generating inventory checklists without needing any cloud provider.

## Usage

```hcl
module "safehouse" {
  source          = "./"
  safehouse_name = "my_safehouse"
  supplies        = ["water", "food", "medicine"]
}
```

Run `terraform init && terraform apply` and the module will create a folder `my_safehouse` with files `water.txt`, `food.txt`, `medicine.txt` containing placeholder text.

## Variables

- `safehouse_name` – Name of the safe‑house directory (default: "safehouse").
- `supplies` – List of supply names to create files for (default: []).

## Outputs

- `safehouse_path` – Absolute path to the created safe‑house directory.
