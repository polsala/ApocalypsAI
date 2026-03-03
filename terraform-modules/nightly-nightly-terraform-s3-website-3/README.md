# nightly-terraform-s3-website

Terraform module that creates an AWS S3 bucket configured for static website hosting. It allows you to set the bucket name, index and error documents, and optionally enable versioning. Ideal for quickly deploying simple static sites without writing Terraform from scratch.

## Usage

```hcl
module "static_site" {
  source          = "./src"
  bucket_name     = "my-static-site-bucket"
  index_document  = "index.html"
  error_document  = "error.html"
  versioning      = true
}
```

## Variables

- `bucket_name` (string, required): Name of the S3 bucket.
- `index_document` (string, default: "index.html"): Index document for website.
- `error_document` (string, default: "error.html"): Error document for website.
- `versioning` (bool, default: false): Enable S3 bucket versioning.

## Outputs

- `bucket_id`: ID of the created bucket.
- `website_endpoint`: Website endpoint URL.

## License

MIT
