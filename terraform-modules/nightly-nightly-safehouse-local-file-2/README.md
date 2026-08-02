# Nightly Safehouse Local File Terraform Module

Creates a local file with customizable content and a random suffix, useful for generating configuration snippets in post‑apocalyptic automation scripts.

## Usage

```hcl
module "safehouse_file" {
  source    = "./utils/nightly-safehouse-local-file"
  file_path = "output/config.txt"
  content   = "Welcome to the safehouse"
}
```

## Variables

- `file_path` (string) – Base path of the file to create.
- `content` (string) – Content to write into the file.

## Outputs

- `full_path` – The full path of the created file (including random suffix).
- `random_suffix` – The random suffix added to the file name.

## Testing

Run the test script:

```sh
cd utils/nightly-safehouse-local-file
bash tests/test_module.sh
```
