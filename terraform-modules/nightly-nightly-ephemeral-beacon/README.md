# Nightly Ephemeral Beacon

A Terraform module for deploying whimsical, short-lived "ephemeral beacons" in AWS. These beacons are designed to perform quick, distributed tasks or health checks and can optionally self-terminate upon completion, minimizing resource consumption and embodying the transient nature of post-apocalyptic scouting.

## 🌟 Whimsical Purpose

In the vast, unpredictable wasteland, sometimes you just need a quick signal flare, a momentary scout, or a burst of computational energy to check for anomalies or perform a swift task. The Ephemeral Beacon is your answer – a fleeting whisper in the cloud, delivering its message and then fading into the digital ether.

## 🛠️ Technical Utility

This module provisions AWS EC2 instances that execute a user-defined bash script upon launch. Key features include:
- **Ephemeral Design**: Ideal for burstable workloads, quick checks, or tasks that don't require persistent infrastructure.
- **Self-Termination**: Beacons can be configured to automatically shut down after their task is complete, saving costs.
- **Distributed Tasks**: Easily deploy multiple beacons to perform parallel operations across different zones or regions.
- **Log Collection**: Optionally upload task logs to an S3 bucket for post-mortem analysis.
- **IAM Role**: Automatically creates an IAM role with necessary permissions for self-termination and S3 logging.

## 🚀 Usage

To deploy your own Ephemeral Beacons, include this module in your Terraform configuration:

```terraform
module "my_ephemeral_beacon_network" {
  source = "polsala/ApocalypsAI//terraform-modules/nightly-ephemeral-beacon" # Adjust path if using locally

  region             = "us-east-1"
  instance_type      = "t3.nano"
  ami_id             = null # Set to a valid AMI ID, or leave null to auto-select Amazon Linux 2
  key_name           = "my-ssh-key"           # Optional: Your EC2 Key Pair name for SSH access
  beacon_count       = 3                      # Deploy 3 beacons
  security_group_ids = ["sg-0123456789abcdef0"] # Replace with your security group ID allowing outbound access

  task_script = <<-EOT
    echo "Beacon $${count.index} reporting in!"
    ping -c 3 google.com
    echo "Beacon $${count.index} task complete."
  EOT

  self_terminate  = true
  log_bucket_name = "my-apocalypsai-beacon-logs" # Optional: An existing S3 bucket name
}

output "beacon_ips" {
  value = module.my_ephemeral_beacon_network.beacon_public_ips
}
```

### Prerequisites

1.  **AWS Account & Credentials**: Ensure your AWS credentials are configured for Terraform (e.g., via environment variables, `~/.aws/credentials`, or IAM roles).
2.  **Terraform CLI**: Install Terraform (v1.0+ recommended).
3.  **AMI ID**: Provide a valid AMI ID for your chosen `region`. If `ami_id` is `null`, the module will attempt to find the latest Amazon Linux 2 AMI.
4.  **Security Group**: Create a security group that allows outbound internet access for your beacons to perform tasks like `ping` or `curl`.

### Inputs

| Name                | Description                                                                                             | Type        | Default                                                                 | Required |
| :------------------ | :------------------------------------------------------------------------------------------------------ | :---------- | :---------------------------------------------------------------------- | :------- |
| `region`            | The AWS region to deploy the beacons.                                                                   | `string`    | `"us-east-1"`                                                           | no       |
| `instance_type`     | The EC2 instance type for the beacons.                                                                  | `string`    | `"t3.micro"`                                                            | no       |
| `ami_id`            | The AMI ID to use for the beacons. If `null`, a recent Amazon Linux 2 AMI will be selected.             | `string`    | `null`                                                                  | no       |
| `key_name`          | The name of the EC2 Key Pair to allow SSH access to the beacons (optional, but recommended for debugging). | `string`    | `null`                                                                  | no       |
| `beacon_count`      | The number of ephemeral beacons to deploy.                                                              | `number`    | `1`                                                                     | no       |
| `task_script`       | The bash script or command to execute on each beacon. This will be run after startup.                   | `string`    | `"echo 'No specific task defined. Beacon is just observing the void.'"` | no       |
| `self_terminate`    | If `true`, the beacon instances will attempt to terminate themselves after the task script completes.   | `bool`      | `true`                                                                  | no       |
| `log_bucket_name`   | Optional: The name of an S3 bucket to upload beacon logs to. If `null`, logs are only local.            | `string`    | `null`                                                                  | no       |
| `security_group_ids`| A list of security group IDs to associate with the beacon instances. Required for network access.       | `list(string)`| `[]`                                                                    | yes      |

### Outputs

| Name                  | Description                                                               |
| :-------------------- | :------------------------------------------------------------------------ |
| `beacon_public_ips`   | A list of public IP addresses of the deployed ephemeral beacons.          |
| `beacon_instance_ids` | A list of instance IDs of the deployed ephemeral beacons.                 |
| `beacon_iam_role_name`| The name of the IAM role created for the beacons.                         |

## 🧪 Testing

The module includes a `tests/test_module.sh` script that performs offline validation:
1.  Initializes Terraform in a temporary directory.
2.  Validates the module's syntax using `terraform validate`.
3.  Generates a `terraform plan` and asserts on its output to ensure expected resources (e.g., `aws_instance`) are planned for creation with correct properties.

To run the tests:
```bash
cd terraform-modules/nightly-ephemeral-beacon
./tests/test_module.sh
```

## ⚠️ Important Considerations

-   **IAM Permissions**: The created IAM role grants `ec2:TerminateInstances` and `s3:PutObject` permissions. In a production environment, consider scoping these permissions down to specific resources.
-   **Security Groups**: Ensure the `security_group_ids` provided allow necessary outbound traffic for your `task_script` to function.
-   **AMI Selection**: If `ami_id` is `null`, the module selects the latest Amazon Linux 2 AMI. Verify this AMI is suitable for your tasks.
-   **Spot Instances**: For even greater ephemerality and cost savings, you could modify `main.tf` to use `aws_spot_instance_request` instead of `aws_ec2_instance`. This would make the beacons truly transient and subject to AWS's spot market.
