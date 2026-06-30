# Nightly Cloud-Whisperer Beacon

## Summary
This Terraform module provisions a whimsical AWS S3 bucket configured as a static website, ready to broadcast community whispers or status updates to the digital void.

## Purpose
In the ever-shifting landscape of the apocalypse, a stable point of communication is vital. This beacon provides a simple, low-cost way to establish a public-facing endpoint where the community can share messages, updates, or simply existential musings. It's a digital campfire for the end times.

## Usage

1.  **Prerequisites**:
    *   [Terraform](https://www.terraform.io/downloads.html) installed.
    *   AWS credentials configured (e.g., via `~/.aws/credentials` or environment variables).
    *   `jq` installed (for running tests).

2.  **Module Integration**:
    Create a new Terraform configuration file (e.g., `main.tf`) in your project and reference this module:

    ```terraform
    module "whisper_beacon" {
      source = "./path/to/nightly-cloud-whisperer-beacon/src"

      # Optional: Customize these variables
      bucket_name_prefix    = "my-community-beacon"
      region                = "us-west-2"
      initial_whisper_message = "Hear ye, hear ye! The latest news from Sector 7G: The squirrels are organizing."
    }

    output "beacon_url" {
      value = module.whisper_beacon.website_endpoint
    }
    ```

3.  **Deployment**:
    Navigate to your project directory (where your `main.tf` is located) and run:

    ```bash
    terraform init
    terraform plan
    terraform apply
    ```

    Confirm the `apply` operation when prompted.

4.  **Accessing the Beacon**:
    After successful deployment, Terraform will output the `beacon_url`. You can access your whimsical static website through this URL.

## Inputs

| Name                    | Description                                                              | Type   | Default                                                                                              | Required |
| :---------------------- | :----------------------------------------------------------------------- | :----- | :--------------------------------------------------------------------------------------------------- | :------- |
| `bucket_name_prefix`    | A prefix for the S3 bucket name. A random suffix will be appended.       | `string` | `"apocalypsai-whisper-beacon"`                                                                     | no       |
| `region`                | The AWS region to deploy the S3 bucket in.                               | `string` | `"us-east-1"`                                                                                      | no       |
| `initial_whisper_message` | The initial whimsical message to display on the beacon's index page.     | `string` | `"Greetings, wanderer! May your path be ever-illuminated by the glow of forgotten stars."`         | no       |

## Outputs

| Name             | Description                                  |
| :--------------- | :------------------------------------------- |
| `website_endpoint` | The URL of the static website endpoint.      |
| `bucket_name`    | The full name of the S3 bucket.              |

## Tests

The `tests/test.sh` script performs offline validation and planning checks to ensure the module is correctly configured and produces the expected resources without deploying actual infrastructure. It uses `terraform validate` and `terraform plan -json` to inspect the planned changes.
