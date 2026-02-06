# Nightly Wasteland Scrap Bucket

Terraform module that provisions a whimsical "scrap" S3 bucket with a lifecycle rule that automatically deletes objects older than 30 days. Ideal for post‑apocalypse data hoarding or temporary storage of scavenged artifacts.

## Usage

```hcl
module "scrap_bucket" {
  source      = "github.com/yourorg/polsala/ApocalypsAI//terraform-modules/nightly-wasteland-scrap-bucket"
  bucket_name = "my-scrap-bucket"
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| bucket_name | Name of the S3 bucket to create | string | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| bucket_id | The ID of the created S3 bucket |

## Testing

Run the provided test script:

```sh
cd test
./test_module.sh
```

The script runs `terraform init` and `terraform validate` offline and ensures the lifecycle rule is present.

## License

MIT
