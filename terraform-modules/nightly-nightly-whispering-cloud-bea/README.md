# Nightly Whispering Cloud Beacon

## Summary
This Terraform module deploys a whimsical-yet-useful serverless 'whispering beacon' API endpoint on AWS. It provides a simple HTTP POST endpoint where you can send small, ephemeral messages (or 'whispers') that are then logged to AWS CloudWatch. It's perfect for collecting lightweight events, status updates, or just sending notes into the digital void.

## Features
- **Serverless**: Built with AWS Lambda and API Gateway, meaning no servers to manage.
- **Simple API**: A single POST endpoint (`/whisper`) to send your messages.
- **Ephemeral Logging**: Whispers are logged to CloudWatch, with a configurable retention period.
- **Cost-Effective**: Leverages AWS Free Tier friendly services.
- **Whimsical**: Because even infrastructure can have a personality.

## Usage
To deploy your own Whispering Cloud Beacon, create a `main.tf` file in your Terraform project and use this module:

```terraform
# main.tf

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.0"
}

provider "aws" {
  region = "us-east-1" # Or your preferred AWS region
}

module "my_whisper_beacon" {
  source = "./path/to/nightly-whispering-cloud-beacon/src" # Adjust path as needed

  prefix      = "community-status" # A unique prefix for your resources
  memory_size = 128                # Optional: Lambda memory in MB
  timeout     = 30                 # Optional: Lambda timeout in seconds
  runtime     = "python3.9"        # Optional: Lambda runtime
}

output "beacon_api_endpoint" {
  description = "The URL to send whispers to."
  value       = module.my_whisper_beacon.api_endpoint
}

output "beacon_lambda_name" {
  description = "The name of the deployed Lambda function."
  value       = module.my_whisper_beacon.lambda_function_name
}
```

After setting up your `main.tf`:

1.  Initialize Terraform:
    ```bash
    terraform init
    ```
2.  Plan the deployment:
    ```bash
    terraform plan
    ```
3.  Apply the changes:
    ```bash
    terraform apply
    ```

Once deployed, you can send a whisper using `curl`:

```bash
# Replace <YOUR_API_ENDPOINT> with the actual output value
curl -X POST -H "Content-Type: application/json" \
     -d '{"message": "The stars align for a new utility!"}' \
     "$(terraform output -raw beacon_api_endpoint)"
```

Check your AWS CloudWatch logs for the Lambda function (`<prefix>-whisper-collector`) to see your whispers being collected.

## Inputs
| Name        | Description                                           | Type   | Default         | Required |
| :---------- | :---------------------------------------------------- | :----- | :-------------- | :------- |
| `prefix`    | A unique prefix for all resources created by this module. | `string` | `"beacon"`      | no       |
| `memory_size` | The amount of memory in MB your Lambda Function can use at runtime. | `number` | `128`           | no       |
| `timeout`   | The amount of time your Lambda Function has to run in seconds. | `number` | `30`            | no       |
| `runtime`   | The identifier of the function's runtime.             | `string` | `"python3.9"`   | no       |

## Outputs
| Name                 | Description                                    |
| :------------------- | :--------------------------------------------- |
| `api_endpoint`       | The URL of the API Gateway endpoint for sending whispers. |
| `lambda_function_name` | The name of the deployed Lambda function.      |

## Testing
This module includes automated tests using `terraform test`. To run them:

```bash
terraform test
```

Tests are deterministic and offline, using `mock_provider` to simulate AWS resource creation without actual deployment. This ensures fast and reliable validation of the module's configuration.
