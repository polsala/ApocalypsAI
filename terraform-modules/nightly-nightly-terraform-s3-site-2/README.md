# Terraform S3 Static Site Module

This Terraform module creates an AWS S3 bucket configured for static website hosting.

## Usage

```hcl
module "static_site" {
  source          = "./"
  bucket_name     = "my-website-bucket"
  index_document  = "index.html"
  error_document  = "error.html"
}
```

## Variables

- `bucket_name` (string, required): Name of the S3 bucket.
- `index_document` (string, optional, default `"index.html"`): Index document.
- `error_document` (string, optional, default `"error.html"`): Error document.
- `acl` (string, optional, default `"public-read"`): Canned ACL.

## Outputs

- `bucket_id`
- `bucket_arn`
- `website_endpoint`

## Testing

Run the provided mock test script:

```sh
cd tests && ./test.sh
```
