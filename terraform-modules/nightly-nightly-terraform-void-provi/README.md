# nightly-terraform-void-provisioner

Provision ephemeral cloud infrastructure themed around post-apocalyptic survival. This Terraform module creates temporary resources such as compute instances, object storage buckets, and network rules with a wasteland flair.

## Features

- Creates temporary compute instances with wasteland-themed names
- Provisions object storage with survival gear checklists
- Applies network rules simulating radio blackouts

## Usage

```hcl
module "void_provisioner" {
  source = "./terraform-modules/nightly-terraform-void-provisioner"

  region         = "us-west-1"
  instance_count = 3
  bucket_name    = "wasteland-supplies"
}
```

## Inputs

| Name           | Description                     | Type   | Default |
|----------------|----------------------------------|--------|---------|
| region         | AWS region to deploy resources   | string | n/a     |
| instance_count | Number of compute instances      | number | 1       |
| bucket_name    | Name of the S3 bucket             | string | n/a     |

## Outputs

| Name              | Description                      |
|-------------------|----------------------------------|
| instance_ids      | List of compute instance IDs     |
| bucket_arn        | ARN of the created S3 bucket     |
| security_group_id | ID of the security group         |
