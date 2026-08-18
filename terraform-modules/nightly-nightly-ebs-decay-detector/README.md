# Nightly EBS Decay Detector

This Terraform module helps you identify unattached Amazon EBS (Elastic Block Store) volumes within a specified AWS region. Unattached EBS volumes are often orphaned resources that continue to incur costs and can pose security risks if not properly managed. This module flags them as 'decaying' resources, making it easier for you to review and clean them up.

## Features

- Scans a specified AWS region for EBS volumes with a status of 'available' (i.e., not attached to any EC2 instance).
- Optionally filters volumes by tags.
- Outputs a list of unattached volume IDs, their count, and detailed information.

## Usage

To use this module, include it in your Terraform configuration and provide the necessary inputs.

### Example

```terraform
module "ebs_decay_detector" {
  source = "./path/to/your/module/src" # Adjust this path to where you place the module's src directory

  region = "us-east-1" # Required: The AWS region to scan

  # Optional: Filter by tags. Only volumes matching ALL specified tags will be returned.
  # tags_filter = {
  #   "Environment" = "dev"
  #   "Project"     = "cleanup"
  # }
}

output "decaying_ebs_volumes" {
  description = "Identified unattached EBS volumes."
  value       = module.ebs_decay_detector.unattached_ebs_volumes_details
}

output "decaying_ebs_count" {
  description = "Count of identified unattached EBS volumes."
  value       = module.ebs_decay_detector.unattached_ebs_volumes_count
}
```

### Inputs

| Name        | Description                                                               | Type        | Default     | Required |
|-------------|---------------------------------------------------------------------------|-------------|-------------|----------|
| `region`    | The AWS region to scan for unattached EBS volumes.                        | `string`    | `"us-east-1"` | no       |
| `tags_filter` | A map of tags to filter EBS volumes. Only volumes matching these tags will be considered. | `map(string)` | `{}`        | no       |

### Outputs

| Name                             | Description                                       | Type           |
|----------------------------------|---------------------------------------------------|----------------|
| `unattached_ebs_volume_ids`      | A list of IDs of unattached EBS volumes.          | `list(string)` |
| `unattached_ebs_volumes_count`   | The count of unattached EBS volumes found.        | `number`       |
| `unattached_ebs_volumes_details` | Details of unattached EBS volumes (id, size, type, etc.). | `list(object)` |

## Requirements

- Terraform `v1.0.0` or higher.
- AWS Provider `~> 5.0`.
- Configured AWS credentials with permissions to list EBS volumes (`ec2:DescribeVolumes`).

## Development & Testing

Refer to the `tests/` directory for how to run structural validation tests for this module.
