# Apocalyptic Safehouse S3

Creates an S3 bucket named with a prefix and random suffix, enables versioning, server‑side encryption, and a lifecycle rule to delete old versions after 30 days. Useful for storing community backups in a post‑apocalyptic scenario.

## Usage

```hcl
module "safehouse_s3" {
  source = "git::https://github.com/polsala/ApocalypsAI.git//terraform-modules/nightly-apocalypse-safehouse-s3"
  bucket_name_prefix = "safehouse"
  tags = {
    Environment = "post-apocalypse"
  }
}
```

Run `terraform init && terraform apply`.

## Inputs

- `bucket_name_prefix` (string) – Prefix for bucket name. Default: "apocalypse".
- `tags` (map(string)) – Tags to apply.

## Outputs

- `bucket_name` – The name of the created bucket.

## Testing

```bash
cd tests && ./test.sh
```
