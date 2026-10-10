# Nightly Cloud Constellation Mapper

Chart your cloud cosmos with the Nightly Cloud Constellation Mapper! This Terraform module helps you define logical groupings of your cloud resources, treating them as celestial constellations. It enforces consistent naming prefixes and tagging conventions, making it easier to manage, identify, and observe your infrastructure.

## Features

*   **Constellation Definition**: Define a unique "constellation" name and an environment.
*   **Consistent Naming**: Generates a standardized prefix for resources belonging to the constellation.
*   **Automated Tagging**: Provides a set of essential tags to apply to all resources within the constellation, including the constellation name, environment, and a `ManagedBy` tag.
*   **Whimsical yet Practical**: Brings a touch of cosmic order to your cloud chaos.

## Usage

To use this module, include it in your Terraform configuration and pass the required variables.

```terraform
module "my_constellation" {
  source = "./path/to/nightly-cloud-constellation-mapper/src" # Or a Git/registry source
  
  constellation_name = "Andromeda"
  environment        = "dev"
  additional_tags    = {
    "Owner" = "ApocalypsAI"
  }
}

resource "aws_s3_bucket" "constellation_bucket" {
  bucket = "${module.my_constellation.prefix}-data-store"
  tags   = module.my_constellation.tags
  # ... other bucket configurations
}

output "constellation_prefix" {
  value = module.my_constellation.prefix
}

output "constellation_tags" {
  value = module.my_constellation.tags
}
```

## Inputs

| Name                 | Description                                                               | Type        | Default     | Required |
| :------------------- | :------------------------------------------------------------------------ | :---------- | :---------- | :------- |
| `constellation_name` | The whimsical name for your cloud constellation (e.g., "Orion", "Pegasus"). | `string`    | `""`        | yes      |
| `environment`        | The environment this constellation belongs to (e.g., "dev", "prod", "staging"). | `string`    | `""`        | yes      |
| `additional_tags`    | A map of additional tags to merge with the default constellation tags.    | `map(string)` | `{}`        | no       |

## Outputs

| Name                 | Description                                                               |
| :------------------- | :------------------------------------------------------------------------ |
| `prefix`             | A standardized naming prefix for resources in this constellation (e.g., `andromeda-dev`). |
| `tags`               | A map of tags to apply to all resources within this constellation. Includes `Constellation`, `Environment`, `ManagedBy`, and any `additional_tags`. |

## Development & Testing

The module includes a `tests/` directory with an example configuration and a `test.sh` script to validate its outputs deterministically and offline.

To run tests:

```bash
cd tests
./test.sh
```

**Prerequisites for testing**: `terraform` and `jq` must be installed and available in your PATH.
