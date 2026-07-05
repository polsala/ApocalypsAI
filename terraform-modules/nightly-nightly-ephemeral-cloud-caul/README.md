# Nightly Ephemeral Cloud Cauldron

A Terraform module to conjure temporary, self-destructing AWS S3 buckets for fleeting data experiments and quick-and-dirty storage needs.

## 🧙‍♂️ What it Does

This module provisions an AWS S3 bucket with a built-in lifecycle policy that automatically expires all objects (and the bucket itself, if empty) after a specified number of days. It's perfect for:

*   **Temporary Data Storage:** Need a place to dump some logs or test data for a few days? This cauldron has you covered.
*   **Ephemeral Testing:** Spin up a bucket for a CI/CD test run, knowing it will vanish without a trace.
*   **Cost Control:** Avoid forgotten resources racking up bills. The cauldron cleans itself!
*   **Whimsical Experiments:** Just want to see if you can store a digital pet rock for a week? Go for it!

## 🔮 Usage

To use this module, include it in your Terraform configuration:

```terraform
module "ephemeral_bucket" {
  source = "./nightly-ephemeral-cloud-cauldron/src" # Adjust path as needed
  
  resource_name_prefix = "my-ephemeral-test"
  region               = "us-east-1"
  ttl_days             = 7 # Bucket and its contents will expire after 7 days
  tags = {
    Project     = "ApocalypsAI"
    Environment = "Ephemeral"
    Owner       = "IntegratorAgent"
  }
}

output "bucket_id" {
  value = module.ephemeral_bucket.bucket_id
}

output "bucket_arn" {
  value = module.ephemeral_bucket.bucket_arn
}
```

Then run `terraform init`, `terraform plan`, and `terraform apply`.

## ⚙️ Configuration (Variables)

| Name                 | Description                                                                 | Type     | Default | Required |
| :------------------- | :-------------------------------------------------------------------------- | :------- | :------ | :------- |
| `resource_name_prefix` | A prefix for the S3 bucket name to ensure uniqueness.                       | `string` | `""`    | yes      |
| `region`             | The AWS region where the S3 bucket will be created.                         | `string` | `""`    | yes      |
| `ttl_days`           | The number of days after which objects in the bucket will expire.           | `number` | `7`     | no       |
| `tags`               | A map of tags to apply to the S3 bucket.                                    | `map(string)` | `{}`    | no       |

## 🌟 Outputs

| Name         | Description                               |
| :----------- | :---------------------------------------- |
| `bucket_id`  | The ID (name) of the created S3 bucket.   |
| `bucket_arn` | The ARN of the created S3 bucket.         |

## 🧪 Testing

The module includes a basic test setup that uses `terraform validate` and `terraform plan -json` to ensure the module's syntax is correct and that it plans to create the expected resources with the correct lifecycle policy.

To run tests:

```bash
cd tests
./run_tests.sh
```
