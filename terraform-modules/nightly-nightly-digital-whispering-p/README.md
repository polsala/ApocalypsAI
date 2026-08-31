# Nightly Digital Whispering Post

This Terraform module provisions a whimsical-yet-useful "Digital Whispering Post" – a serverless, ephemeral message board for the community. Users can leave anonymous "whispers" that automatically fade away after 24 hours, mimicking fleeting thoughts carried on the wind.

## Features

*   **Ephemeral Messages:** Whispers are stored in DynamoDB with a Time-To-Live (TTL) of 24 hours, ensuring they disappear automatically.
*   **Serverless Architecture:** Leverages AWS S3 for static website hosting, API Gateway for message submission/retrieval, and Lambda/DynamoDB for backend logic and storage.
*   **Anonymous Posting:** No user authentication required, allowing for truly anonymous messages.
*   **Simple Web Interface:** A basic HTML page provides an interface to post new whispers and view recent ones.
*   **Highly Available:** Built on AWS serverless services for inherent scalability and reliability.

## Architecture

```mermaid
graph TD
    A[User Browser] -->|GET / POST /whispers| B(API Gateway)
    B -->|Invoke| C(AWS Lambda Function)
    C -->|Read/Write| D(AWS DynamoDB Table)
    A -->|GET /index.html| E(AWS S3 Bucket - Static Website)
    E --&gt; F[index.html]
```

## Usage

1.  **Prerequisites:**
    *   [Terraform](https://www.terraform.io/downloads.html) installed.
    *   AWS CLI configured with credentials that have permissions to create S3 buckets, DynamoDB tables, Lambda functions, API Gateway, and IAM roles/policies.

2.  **Module Integration:**
    Create a `main.tf` file in your root Terraform project:

    ```terraform
    provider "aws" {
      region = "us-east-1" # Or your desired AWS region
    }

    module "whispering_post" {
      source = "./path/to/nightly-digital-whispering-post/src"

      project_name        = "my-community-whispers"
      bucket_name         = "my-community-whispers-bucket-12345" # Must be globally unique
      dynamodb_table_name = "MyCommunityWhispersTable"
      whisper_ttl_hours   = 24 # Default is 24 hours
    }

    output "website_url" {
      value       = "http://${module.whispering_post.s3_website_endpoint}"
      description = "The URL of the static website for the whispering post."
    }

    output "api_url" {
      value       = module.whispering_post.api_gateway_invoke_url
      description = "The API Gateway invoke URL for posting/getting whispers."
    }
    ```

    **Important:** The `bucket_name` must be globally unique across all AWS S3 buckets.

3.  **Deploy:**

    ```bash
    terraform init
    terraform plan
    terraform apply
    ```

4.  **Update Frontend:**
    After `terraform apply`, Terraform will output the `website_url` and `api_url`. You need to manually update the `API_GATEWAY_URL` constant in the `index.html` file within your deployed S3 bucket with the `api_url` output. You can do this by downloading `index.html`, editing it, and re-uploading it to the S3 bucket, or by using the AWS S3 console.

    Alternatively, you can modify the `src/web/index.html` file *before* deployment to include the API Gateway URL directly if you know it, or use a Terraform `local-exec` provisioner to update it post-deployment (though this is less ideal for a module).

5.  **Access the Post:**
    Navigate to the `website_url` in your browser to start whispering!

## Module Inputs

| Name                | Description                                                | Type   | Default                       | Required |
| :------------------ | :--------------------------------------------------------- | :----- | :---------------------------- | :------- |
| `project_name`      | A unique name for the project, used as a prefix for resources. | `string` | `"apocalypsai-whisper"`      | no       |
| `bucket_name`       | The name for the S3 bucket hosting the static website.     | `string` | `"apocalypsai-whispering-post-bucket"` | no       |
| `dynamodb_table_name` | The name for the DynamoDB table storing whispers.          | `string` | `"ApocalypsAIWhispers"`      | no       |
| `whisper_ttl_hours` | Time-to-live for whispers in hours.                        | `number` | `24`                          | no       |

## Module Outputs

| Name                    | Description                                  |
| :---------------------- | :------------------------------------------- |
| `s3_website_endpoint`   | The S3 static website endpoint URL.          |
| `api_gateway_invoke_url` | The invoke URL for the API Gateway.          |

## Development & Testing

To run tests, navigate to the utility's root directory and execute `tests/test_module.sh`.

```bash
./tests/test_module.sh
```

This script will perform `terraform init -backend=false` and `terraform validate` to ensure the HCL syntax is correct and the module is well-formed. It also checks for the presence of essential files.
