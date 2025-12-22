# Nightly Terraform AWS S3 Static Website

## Overview

`nightly-terraform-aws-s3-static-website` is a tiny, self‑contained Terraform module that provisions an Amazon S3 bucket ready to serve a static website.  It sets up the bucket, configures the website settings (index and error documents), and optionally enables public read access.

The module is deliberately **whimsical** – it includes a playful “Apocalypse Oasis” theme, but it is fully functional and can be dropped into any Terraform project.

## Features

- Creates an S3 bucket with a configurable name.
- Enables static website hosting with customizable `index_document` and `error_document`.
- Optional public read ACL (useful for public sites).
- Outputs the bucket website endpoint.

## Usage

```hcl
module "apocalypse_oasis" {
  source          = "../terraform-modules/nightly-terraform-aws-s3-static-website"
  bucket_name     = "my‑apocalypse‑oasis"
  index_document  = "index.html"
  error_document  = "error.html"
  public_read     = true
}

output "website_url" {
  value = module.apocalypse_oasis.website_endpoint
}
```

## Variables

| Name            | Type   | Description                                         | Default |
|-----------------|--------|-----------------------------------------------------|---------|
| `bucket_name`   | string | Name of the S3 bucket (must be globally unique).   | n/a     |
| `index_document`| string | The index document for the website (e.g., `index.html`). | `index.html` |
| `error_document`| string | The error document for the website (e.g., `error.html`). | `error.html` |
| `public_read`   | bool   | If `true`, grants public read access to the bucket. | `false` |

## Outputs

| Name               | Description                                 |
|--------------------|---------------------------------------------|
| `bucket_id`        | The ID of the created S3 bucket.            |
| `website_endpoint` | The website endpoint URL (e.g., `http://<bucket>.s3-website-<region>.amazonaws.com`). |

## Testing

A simple test script is provided under `tests/` that runs `terraform init` (backend disabled) and `terraform validate` to ensure the module syntax is correct and that the expected resources are present.

```bash
cd tests && ./test_module.sh
```

## License

MIT – feel free to adapt, remix, and deploy your own apocalypse‑themed static sites!
