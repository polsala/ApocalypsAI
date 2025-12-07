# Nightly Cloud Critter Habitat

A whimsical-yet-useful Terraform module that deploys a minimal, self-contained cloud 'habitat' for a digital critter. This utility is perfect for: 

*   **Testing Infrastructure:** Quickly spin up a basic EC2 instance with logging to validate your monitoring, logging, or security group configurations.
*   **Learning Terraform:** A simple, illustrative example of deploying a basic cloud resource with user data and outputs.
*   **Adding Whimsy:** Give your cloud environment a touch of digital life with a 'critter' that periodically 'chirps' into its logs.

## Features

*   Deploys a single AWS EC2 instance (default: `t2.micro`).
*   Configures a security group allowing SSH access.
*   Includes `user_data` to install a simple bash script 'critter' that logs a message to `/var/log/critter.log` every minute via cron.
*   Creates an AWS CloudWatch Log Group to collect the critter's chirps (requires a CloudWatch agent setup on the instance, which is beyond this module's scope but the log group is ready).
*   Outputs the instance's public IP and the CloudWatch Log Group name.

## Usage

1.  **Configure AWS Credentials:** Ensure your AWS CLI or environment variables are configured with appropriate credentials.

2.  **Initialize Terraform:**
    ```bash
    terraform -chdir=src init
    ```

3.  **Plan the Deployment:** Review the resources Terraform will create.
    ```bash
    terraform -chdir=src plan
    ```

4.  **Apply the Configuration:** Deploy the critter habitat to your AWS account.
    ```bash
    terraform -chdir=src apply
    ```

5.  **Access Outputs:** After `apply`, Terraform will display the outputs:
    ```
    Outputs:

    instance_public_ip = "<your-instance-ip>"
    log_group_name = "/aws/ec2/critter-habitat-<critter_name>"
    ```

6.  **Destroy the Habitat:** When you're done, clean up the resources.
    ```bash
    terraform -chdir=src destroy
    ```

## Inputs

| Name          | Description                               | Type     | Default         | Required |
| :------------ | :---------------------------------------- | :------- | :-------------- | :------- |
| `region`      | AWS region to deploy resources into.      | `string` | `"us-east-1"`   | no       |
| `critter_name`| A unique name for your digital critter.   | `string` | `"WhimsyCritter"` | no       |
| `instance_type`| EC2 instance type for the critter habitat.| `string` | `"t2.micro"`    | no       |
| `ami_id`      | AMI ID for the EC2 instance. If empty, the latest Amazon Linux 2 AMI will be used. | `string` | `""` | no |
| `key_name`    | The name of the EC2 Key Pair to allow SSH access. | `string` | `"default-ssh-key"` | no |

## Outputs

| Name                 | Description                                    |
| :------------------- | :--------------------------------------------- |
| `instance_public_ip` | The public IP address of the deployed EC2 instance. |
| `log_group_name`     | The name of the CloudWatch Log Group where critter chirps are sent. |

## Critter Behavior

The critter is a simple bash script that runs every minute via cron. It logs a message like `[TIMESTAMP] WhimsyCritter chirps happily from its habitat!` to `/var/log/critter.log` on the EC2 instance. You can SSH into the instance (using the `instance_public_ip` and your `key_name`) and `tail -f /var/log/critter.log` to observe its chirps.
