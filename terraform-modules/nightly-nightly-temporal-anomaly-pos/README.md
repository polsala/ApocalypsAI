# Nightly Temporal Anomaly Observation Post

This Terraform module provisions a dedicated, secure cloud instance designed for the vigilant observation of temporal anomalies. It sets up a basic EC2 instance, a security group to allow essential access, and an S3 bucket to securely store anomaly logs. A simple web server is configured to display the latest anomaly readings.

## Features

*   **EC2 Instance**: A minimal compute instance to host the anomaly detection agent.
*   **Security Group**: Configured to allow SSH (port 22) for management and HTTP (port 80) for the anomaly display web interface.
*   **S3 Log Vault**: A dedicated S3 bucket with versioning and encryption for robust storage of temporal anomaly data.
*   **Whimsical Anomaly Detector**: A simple script that generates dummy anomaly readings and serves them via a web server.

## Usage

To deploy your Temporal Anomaly Observation Post, ensure you have Terraform installed and AWS credentials configured.

1.  **Initialize Terraform**: Navigate to the `src` directory and run `terraform init`.
2.  **Review the Plan**: Run `terraform plan` to see the infrastructure that will be created.
3.  **Apply the Configuration**: Execute `terraform apply` to provision the resources.
4.  **Access**: Once deployed, the public IP address of the EC2 instance will be available in the Terraform outputs. You can access the anomaly readings via HTTP on this IP.

### Inputs

| Name          | Description                                   | Type        | Default                 | Required |
| :------------ | :-------------------------------------------- | :---------- | :---------------------- | :------- |
| `region`      | AWS region to deploy resources in.            | `string`    | `us-east-1`             | no       |
| `instance_type` | EC2 instance type.                            | `string`    | `t2.micro`              | no       |
| `ami_id`      | AMI ID for the EC2 instance (Ubuntu 22.04 LTS). | `string`    | `ami-053b0d53d79c65660` | no       |
| `key_name`    | Name of an existing EC2 Key Pair for SSH access. | `string`    | `""`                    | no       |
| `tags`        | A map of tags to apply to all resources.      | `map(string)` | `{}`                    | no       |

### Outputs

| Name                  | Description                                   |
| :-------------------- | :-------------------------------------------- |
| `instance_public_ip`  | The public IP address of the EC2 instance.    |
| `s3_bucket_name`      | The name of the S3 bucket for anomaly logs.   |

## Testing

To ensure the module is correctly configured and adheres to best practices, run the provided test script. This script performs offline validation and plan inspection without deploying any actual cloud resources.

```bash
cd tests
./test_module.sh
```

**Prerequisites for testing**: `terraform` and `jq` must be installed on your system.

## Contributing

Feel free to enhance the anomaly detection capabilities or add more whimsical monitoring features!
