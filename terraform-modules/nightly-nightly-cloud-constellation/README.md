# Nightly Cloud Constellation Projector

## Summary
This Terraform module deploys a temporary AWS API Gateway and a Python Lambda function. When accessed via its public URL, the Lambda function returns a random, whimsical ASCII art "constellation" or an encouraging message, projecting a little bit of joy into the digital void.

It's a fun, low-cost way to deploy a temporary, public-facing message or art piece in the cloud.

## Prerequisites
*   An AWS account with configured credentials (e.g., via `~/.aws/credentials` or environment variables).
*   Terraform CLI installed (version 1.0+).
*   Python 3.9+ (for local Lambda packaging).

## Deployment
1.  **Navigate to the module directory**:
    ```bash
    cd nightly-cloud-constellation
    ```

2.  **Initialize Terraform**:
    ```bash
    terraform init
    ```

3.  **Review the plan** (optional but recommended):
    ```bash
    terraform plan
    ```

4.  **Apply the configuration**:
    ```bash
    terraform apply
    ```
    Confirm with `yes` when prompted.

## Accessing Your Constellation
After successful deployment, Terraform will output a `constellation_url`. Copy this URL and paste it into your web browser or use `curl`:

```bash
curl $(terraform output -raw constellation_url)
```

Each time you refresh the page or run `curl`, you'll get a new random constellation!

## Cleanup
Since this is a temporary art installation, remember to tear it down when you're done to avoid incurring AWS costs.

1.  **Destroy the resources**:
    ```bash
    terraform destroy
    ```
    Confirm with `yes` when prompted.

This will remove all AWS resources created by this module.
