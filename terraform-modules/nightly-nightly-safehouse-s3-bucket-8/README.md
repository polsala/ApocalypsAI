# Nightly Safehouse S3 Bucket

Creates an S3 bucket (simulated) with versioning and lifecycle for post‑apocalyptic safe‑house data. Uses the `null` and `local` providers to avoid real AWS calls, suitable for CI testing.

## Usage

```hcl
module "safehouse" {
  source      = "./"
  bucket_name = "my-safehouse"
}
```

Run `terraform init` and `terraform apply -auto-approve` to generate a placeholder file `safehouse.txt` representing the bucket.

## Inputs

- `bucket_name` (string) – Name of the safe‑house bucket.

## Outputs

- `bucket_path` – Path to the generated placeholder file.

## Testing

```bash
cd tests && ./validate.sh
```
