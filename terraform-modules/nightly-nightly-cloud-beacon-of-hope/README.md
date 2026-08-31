# Nightly Cloud Beacon of Hope

## Summary
This Terraform module provisions a simple, low-cost static website on AWS S3 and CloudFront. It's designed to serve as a resilient 'beacon of hope' – a community message board, status update hub, or a repository for vital information in the post-apocalyptic landscape.

## Features
*   **Static Website Hosting**: Utilizes AWS S3 for highly available and scalable static content storage.
*   **Global Content Delivery**: Leverages AWS CloudFront for a Content Delivery Network (CDN), ensuring fast access and HTTPS encryption globally.
*   **Secure Access**: Configures CloudFront Origin Access Control (OAC) to restrict direct S3 bucket access, enhancing security.
*   **Customizable**: Easily configure project name, environment, index, and error documents.

## Prerequisites
Before you begin, ensure you have the following installed and configured:
*   **Terraform CLI**: [Install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
*   **AWS CLI**: [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
*   **AWS Credentials**: Configure your AWS credentials with sufficient permissions to create S3 buckets, CloudFront distributions, and IAM policies. A typical set of permissions would include `s3:*`, `cloudfront:*`, `iam:PutRolePolicy`, `iam:AttachRolePolicy`, `iam:CreateRole`, `iam:GetPolicy`, `iam:GetPolicyVersion`, `iam:ListPolicyVersions`, `iam:ListAttachedRolePolicies`, `iam:ListRolePolicies`, `iam:ListRoles`.

## Usage
1.  **Initialize Terraform**: Navigate to the `src` directory and initialize Terraform.
    ```bash
    cd src
    terraform init
    ```

2.  **Review the Plan**: See what resources Terraform will create.
    ```bash
    terraform plan
    ```

3.  **Apply the Configuration**: Deploy the infrastructure.
    ```bash
    terraform apply
    ```
    Confirm with `yes` when prompted.

4.  **Access the Beacon**: After successful application, Terraform will output the `cloudfront_url`. You can access your beacon via this URL.

5.  **Deploy Content**: To deploy your static website content (e.g., `index.html`, `error.html`, CSS, JS, images), upload them to the S3 bucket named in the `s3_bucket_name` output. You can use the AWS CLI:
    ```bash
    aws s3 cp --recursive ./your-website-content/ s3://$(terraform output -raw s3_bucket_name)/
    ```
    Replace `./your-website-content/` with the path to your local website files.

6.  **Destroy the Infrastructure**: When the beacon is no longer needed, you can tear down all resources.
    ```bash
    terraform destroy
    ```
    Confirm with `yes` when prompted.

## Inputs
| Name            | Description                                                | Type   | Default       |
|-----------------|------------------------------------------------------------|--------|---------------|
| `project_name`  | A unique name for the project, used as a prefix for resources. | `string` | `"apocalypsai"` |
| `env`           | The environment (e.g., 'prod', 'dev', 'staging').        | `string` | `"prod"`      |
| `index_document`| The default document for the website (e.g., index.html).   | `string` | `"index.html"`|
| `error_document`| The error document for the website (e.g., error.html).     | `string` | `"error.html"`|

## Outputs
| Name                     | Description                                                |
|--------------------------|------------------------------------------------------------|
| `s3_bucket_name`         | The name of the S3 bucket hosting the beacon content.      |
| `cloudfront_domain_name` | The domain name of the CloudFront distribution for the beacon. |
| `cloudfront_url`         | The full HTTPS URL of the CloudFront distribution.         |
