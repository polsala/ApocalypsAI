# nightly-terraform-s3-site

## Overview

A tiny, selfâcontained Terraform module that provisions an Amazon S3 bucket ready to serve a static website. It configures the bucket for website hosting, sets public read permissions, and optionally allows you to specify custom index and error documents.

## Features

- Creates an S3 bucket with `website` configuration
- Optional `index_document` and `error_document` variables (defaults to `index.html` / `error.html`)
- Public read bucket policy so the site is reachable from the internet
- Outputs the bucket ID and the website endpoint URL

## Usage

```hcl
module "static_site" {
  source          = "./"  # or a registry path if published
  bucket_name     = "myâawesomeâsite"
  index_document  = "index.html"   # optional
  error_document  = "error.html"   # optional
  region          = "us-east-1"    # optional, defaults to us-east-1
}

output "site_url" {
  value = module.static_site.website_endpoint
}
```

## Variables

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| `bucket_name` | Name of the S3 bucket (must be globally unique) | `string` | n/a | yes |
| `index_document` | Index document for the website | `string` | `"index.html"` | no |
| `error_document` | Error document for the website | `string` | `"error.html"` | no |
| `region` | AWS region to create resources in | `string` | `"us-east-1"` | no |

## Outputs

| Name | Description |
|------|-------------|
| `bucket_id` | The ID of the created S3 bucket |
| `website_endpoint` | The website endpoint URL (e.g., `http://bucket.s3-website-us-east-1.amazonaws.com`) |

## Testing

A simple offline test script is provided under `tests/test_main.sh`. It validates that the required Terraform files exist and contain the expected resource definitions. Run it with:

```bash
chmod +x tests/test_main.sh
./tests/test_main.sh
```

## License

MIT â see LICENSE file in the repository root.

