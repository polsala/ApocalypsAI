# Nightly Cloud Beacon

## Summary
This Terraform module deploys a whimsical, low-cost static website beacon in AWS S3. It's designed to serve as a simple, always-on signal of presence in the digital ether, a digital heartbeat, or a basic public status endpoint for your ApocalypsAI infrastructure.

## Whimsical Purpose
In the vast, often silent, digital wasteland, sometimes you just need to know someone's out there. The Cloud Beacon sends a tiny, persistent signal, a digital "hello world" to confirm existence and resilience. It's a comforting hum in the cloud, a reminder that even in the apocalypse, our systems persist.

## Useful Purpose
Beyond its whimsical charm, this module provides a genuinely useful, highly available, and cost-effective resource:
- **Heartbeat/Canary**: A simple, public endpoint to monitor for system uptime and responsiveness.
- **Status Page**: A minimal page to display a static status message.
- **Presence Indicator**: Confirms that your AWS account and basic infrastructure are operational.
- **Low Cost**: Utilizes AWS S3 static website hosting, which is extremely economical.

## Usage
To deploy your own Nightly Cloud Beacon, include this module in your Terraform configuration:

```terraform
module "apocalypsai_beacon" {
  source = "./path/to/nightly-cloud-beacon/src" # Adjust path as necessary

  bucket_name = "your-unique-beacon-bucket-name" # Must be globally unique
  aws_region  = "us-east-1"                      # Or your desired AWS region
  tags = {
    Environment = "Production"
    Project     = "ApocalypsAI"
    Owner       = "IntegratorAgent"
  }
}

output "beacon_url" {
  description = "The URL of the deployed Cloud Beacon website."
  value       = module.apocalypsai_beacon.website_endpoint
}
```

Run `terraform init`, `terraform plan`, and `terraform apply` to deploy the beacon.

## Inputs
| Name        | Description                                                 | Type        | Default     | Required |
|-------------|-------------------------------------------------------------|-------------|-------------|----------|
| `bucket_name` | The name of the S3 bucket for the static website beacon. Must be globally unique. | `string`    | n/a         | yes      |
| `aws_region`  | The AWS region where the S3 bucket will be created.         | `string`    | `us-east-1` | no       |
| `tags`        | A map of tags to assign to the S3 bucket.                   | `map(string)` | `{}`        | no       |

## Outputs
| Name             | Description                                   |
|------------------|-----------------------------------------------|
| `website_endpoint` | The S3 static website endpoint URL.           |
| `bucket_name`      | The name of the S3 bucket created.            |
| `bucket_arn`       | The ARN of the S3 bucket created.             |

## Testing
To run the automated tests for this module, navigate to the `tests/` directory and execute the `test.sh` script.

```bash
cd nightly-cloud-beacon/tests/
./test.sh
```

The tests perform offline validation using `terraform init -backend=false`, `terraform validate`, and `terraform plan -destroy` to ensure the module's syntax is correct and a deployment plan can be generated without actual cloud interaction.
