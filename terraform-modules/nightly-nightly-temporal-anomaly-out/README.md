# Nightly Temporal Anomaly Outpost

This Terraform module deploys a whimsical yet functional "Temporal Anomaly Outpost" in AWS. Its purpose is to provide a dedicated, always-on sentinel that theoretically monitors for temporal distortions, cosmic instability, or just ensures your cloud infrastructure is capable of running a simple cron job.

While its primary function is to humorously detect "anomalies," it serves as a practical example of deploying a basic AWS EC2 instance with a custom user data script to set up a recurring task (a cron job).

## Features

*   **AWS EC2 Instance**: Provisions a t2.micro EC2 instance (configurable).
*   **Security Group**: Creates a minimal security group allowing SSH access (configurable).
*   **User Data Script**: Installs a simple "Temporal Anomaly Detector" script that runs via cron every 5 minutes, logging its "findings."
*   **Configurable**: Allows customization of region, instance type, AMI, and key pair.

## Usage

1.  **Prerequisites**:
    *   [Terraform](https://www.terraform.io/downloads.html) installed.
    *   AWS credentials configured (e.g., via `~/.aws/credentials` or environment variables).

2.  **Module Integration**:
    Create a `main.tf` file in your project:

    ```terraform
    module "temporal_outpost" {
      source = "./nightly-temporal-anomaly-outpost" # Or a Git/S3 source if published

      aws_region      = "us-east-1"
      instance_type   = "t2.micro"
      ami_id          = "ami-053b0d53c279acc90" # Example: Amazon Linux 2 AMI (HVM), SSD Volume Type
      key_name        = "my-ssh-key"           # Replace with your EC2 Key Pair name
      allowed_cidrs   = ["0.0.0.0/0"]          # WARNING: Broad access, restrict in production!
      outpost_name    = "TemporalAnomalyDetector-001"
    }

    output "outpost_public_ip" {
      description = "The public IP address of the Temporal Anomaly Outpost."
      value       = module.temporal_outpost.public_ip
    }
    ```

    **Note on `ami_id`**: The provided AMI ID is an example for `us-east-1` (Amazon Linux 2). You should find an appropriate AMI for your chosen `aws_region`.

3.  **Initialize Terraform**:

    ```bash
    terraform init
    ```

4.  **Review the Plan**:

    ```bash
    terraform plan
    ```

5.  **Deploy the Outpost**:

    ```bash
    terraform apply
    ```

    Confirm with `yes` when prompted.

6.  **Access the Outpost (Optional)**:
    Once deployed, you can SSH into the instance using the public IP from the output and your specified key:

    ```bash
    ssh -i /path/to/my-ssh-key.pem ec2-user@<OUTPOST_PUBLIC_IP>
    ```
    You can then check the anomaly detector logs:
    ```bash
    tail -f /var/log/temporal_anomaly_detector.log
    ```

7.  **Destroy the Outpost**:
    When you're done, clean up the resources:

    ```bash
    terraform destroy
    ```

## Module Inputs

| Name            | Description                                     | Type     | Default     |
| :-------------- | :---------------------------------------------- | :------- | :---------- |
| `aws_region`    | AWS region to deploy resources into.            | `string` | n/a         |
| `instance_type` | EC2 instance type.                              | `string` | `"t2.micro"`|
| `ami_id`        | AMI ID for the EC2 instance.                    | `string` | n/a         |
| `key_name`      | Name of the EC2 Key Pair for SSH access.        | `string` | n/a         |
| `allowed_cidrs` | List of CIDR blocks allowed to SSH into the outpost.| `list(string)` | `["0.0.0.0/0"]` |
| `outpost_name`  | Name tag for the EC2 instance and security group. | `string` | `"TemporalAnomalyOutpost"` |

## Module Outputs

| Name            | Description                                     |
| :-------------- | :---------------------------------------------- |
| `public_ip`     | The public IP address of the EC2 instance.      |
| `instance_id`   | The ID of the EC2 instance.                     |
| `security_group_id` | The ID of the created security group.       |

## Testing

The module includes a `tests/` directory with a `test_module.tf` configuration and a `run_tests.sh` script. These tests validate the Terraform syntax and ensure a plan can be generated without errors, simulating a deployment without actually provisioning resources.

To run tests:

```bash
cd tests
./run_tests.sh
```
