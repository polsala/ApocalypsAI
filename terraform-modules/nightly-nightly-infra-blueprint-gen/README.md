## Nightly Infra Blueprint Generator

This Terraform module generates a basic infrastructure blueprint for a simple web server, including an EC2 instance, a security group, and an S3 bucket for static content.

### Usage

To use this module, include it in your Terraform configuration:

```hcl
module "web_server_infra" {
  source = "./path/to/this/module"

  instance_type = "t2.micro"
  ami_id        = "ami-0abcdef1234567890" # Replace with a valid AMI ID for your region
  bucket_name   = "my-unique-web-content-bucket"
}
```

### Variables

*   `instance_type` (string, optional): The EC2 instance type. Defaults to `t2.micro`.
*   `ami_id` (string, required): The AMI ID for the EC2 instance. **You must provide a valid AMI ID for your AWS region.**
*   `bucket_name` (string, required): A unique name for the S3 bucket.

### Outputs

*   `instance_id`: The ID of the created EC2 instance.
*   `security_group_id`: The ID of the created security group.
*   `bucket_name`: The name of the created S3 bucket.
