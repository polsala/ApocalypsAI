# nightly-terraform-quickstart

A minimal Terraform module that provisions an S3 bucket with versioning and lifecycle rules, ready for quick starts.

## Usage

```hcl
module \"quickstart\" {
  source = \"git::https://github.com/polsala/ApocalypsAI.git//terraform-modules/nightly-terraform-quickstart\"

  bucket_name = \"my-quickstart-bucket\"
  region      = \"us-east-1\"
}
```

## Features

- Creates an S3 bucket with versioning enabled.
- Adds a lifecycle rule that expires objects older than 30 days.
- Outputs the bucket ID and ARN.

## Example

```hcl
terraform init
terraform apply
```

Happy Terraforming! 🚀
