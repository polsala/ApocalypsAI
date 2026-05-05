# Nightly Apocalypse Name Generator

A tiny Terraform module that generates a list of whimsical, apocalypse‑themed names using the `random_pet` resource. Perfect for giving your cloud resources memorable identifiers.

## Usage

```hcl
module "apoc_names" {
  source = "./"
  count  = 5
}

output "names" {
  value = module.apoc_names.names
}
```

## Inputs

- `count` (number, default 3): How many names to generate.

## Outputs

- `names` (list(string)): Generated names, each prefixed with `apoc-`.

## Example

Running `terraform apply` will output something like:

```
names = [
  "apoc-ancient-wolf",
  "apoc-bleak-owl",
  "apoc-cryptic-raven",
]
```
