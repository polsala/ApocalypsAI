# Nightly Apocalyptic Tagger

A Terraform module designed to bring a touch of post-apocalyptic whimsy to your AWS resource management, while enforcing crucial tagging and naming conventions. This module helps you apply consistent, apocalypse-themed tags and generates unique, thematic names for your cloud resources, ensuring both operational clarity and a bit of fun in the desolate digital landscape.

## Features

*   **Whimsical Naming**: Generates unique resource names based on a prefix, resource type, environment, and a selection of apocalyptic themes.
*   **Consistent Tagging**: Automatically applies a set of predefined, apocalypse-themed tags for better resource organization, cost allocation, and operational insights.
*   **AWS Provider Agnostic**: Designed to work with any AWS resource that accepts `tags` and `name` attributes.

## Usage

To use this module, include it in your Terraform configuration and pass the required variables.

```terraform
module "apocalyptic_instance" {
  source = "./src" # Adjust this path based on where you place the module's 'src' directory
  
  resource_name_prefix = "sentry"
  resource_type        = "EC2-Instance"
  environment          = "dev"
}

resource "aws_instance" "my_sentry_instance" {
  ami           = "ami-0abcdef1234567890" # Replace with a valid AMI for your region
  instance_type = "t2.micro"
  
  # Merge the generated tags with the 'Name' tag for the resource
  tags = merge(module.apocalyptic_instance.generated_tags, {
    Name = module.apocalyptic_instance.generated_name
  })
}

output "instance_name" {
  value = module.apocalyptic_instance.generated_name
}

output "instance_tags" {
  value = module.apocalyptic_instance.generated_tags
}
```

## Module Inputs

| Name                 | Description                                       | Type     | Default | Required |
| :------------------- | :------------------------------------------------ | :------- | :------ | :------- |
| `resource_name_prefix` | A short prefix for the resource name.             | `string` | n/a     | yes      |
| `resource_type`      | The type of resource (e.g., "EC2-Instance", "RDS-DB"). | `string` | n/a     | yes      |
| `environment`        | The deployment environment (e.g., "dev", "prod", "staging"). | `string` | n/a     | yes      |

## Module Outputs

| Name             | Description                                       |
| :--------------- | :------------------------------------------------ |
| `generated_name` | The whimsically generated name for the resource.  |
| `generated_tags` | A map of apocalypse-themed tags for the resource. |

## Development & Testing

This module includes a self-contained test setup to verify its logic without provisioning actual cloud resources. The tests are designed to be deterministic and offline.

To run the tests:

1.  Navigate to the `tests/` directory.
2.  Execute the test script: `./test_apocalyptic_tagger.sh`

The script will initialize Terraform, run a plan, and assert expected outputs based on the module's internal logic.
