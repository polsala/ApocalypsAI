# Nightly Temporal Beacon

A Terraform module that deploys a "Temporal Beacon" – a resilient, tagged cloud resource designed to maintain a stable presence amidst infrastructure chaos. In the ever-shifting sands of the post-apocalyptic cloud, this beacon acts as a chronal anchor, ensuring a critical point of reference remains operational and identifiable.

## Features

*   **Chronal Anchoring**: Deploys a core EC2 instance that serves as your temporal beacon.
*   **Reality Stabilizer Tagging**: Automatically applies a `ChronalAnchor` tag with a configurable value, making it easy to identify your stable points.
*   **Configurable Resilience**: Allows selection of instance type and AMI to suit various stability needs.
*   **Whimsical Naming**: Embrace the chaos with fun, thematic naming conventions.

## Usage

To deploy a Temporal Beacon, include this module in your Terraform configuration:

```terraform
module "temporal_beacon_alpha" {
  source = "./nightly-temporal-beacon/src" # Adjust path if not in same repo
  
  region                     = "us-east-1"
  instance_type              = "t2.micro"
  ami_id                     = "ami-0abcdef1234567890" # Replace with a valid AMI for your region
  beacon_name                = "AlphaSectorStabilizer"
  chronal_anchor_tag_value   = "PrimaryTimelineAnchor"
}

output "alpha_beacon_id" {
  value = module.temporal_beacon_alpha.instance_id
}

output "alpha_beacon_public_ip" {
  value = module.temporal_beacon_alpha.public_ip
}
```

### Inputs

| Name                       | Description                                                              | Type     | Default | Required |
| :------------------------- | :----------------------------------------------------------------------- | :------- | :------ | :------- |
| `region`                   | The AWS region to deploy the beacon in.                                  | `string` | n/a     | yes      |
| `instance_type`            | The EC2 instance type for the temporal beacon.                           | `string` | n/a     | yes      |
| `ami_id`                   | The AMI ID to use for the EC2 instance.                                  | `string` | n/a     | yes      |
| `beacon_name`              | A whimsical name for your temporal beacon.                               | `string` | n/a     | yes      |
| `chronal_anchor_tag_value` | The value for the `ChronalAnchor` tag, identifying its stabilization role. | `string` | n/a     | yes      |

### Outputs

| Name             | Description                                |
| :--------------- | :----------------------------------------- |
| `instance_id`    | The ID of the deployed EC2 instance.       |
| `public_ip`      | The public IP address of the EC2 instance. |

## Development & Testing

This module includes a self-contained test suite that uses `terraform plan` to verify the module's output without deploying actual resources.

To run tests:

```bash
cd tests
./test_temporal_beacon.sh
```

The test script will:
1. Initialize Terraform in the test environment.
2. Run `terraform plan` to simulate deployment.
3. Assert that the plan output contains expected resources and tags.
