# Nightly Ephemeral Message Drop

This Terraform module deploys a temporary AWS EC2 instance running Nginx, serving a custom message, and configured to self-destruct after a specified time. It's ideal for quick, anonymous, and transient communication in the wasteland, leaving no persistent traces.

## Features

*   **Ephemeral Nature**: Instances are configured to automatically shut down after a set number of minutes.
*   **Custom Messages**: Easily deploy a simple web server with your custom message.
*   **Simple Deployment**: Leverages AWS EC2, Security Groups, and User Data for straightforward provisioning.
*   **Secure by Default (for ephemeral)**: Only HTTP (80) and SSH (22) ports are opened to the world (0.0.0.0/0), but remember to use strong SSH keys and consider restricting SSH access further in production scenarios.

## Usage

1.  **Prerequisites**:
    *   [Terraform](https://www.terraform.io/downloads.html) installed.
    *   AWS credentials configured (e.g., via `~/.aws/credentials` or environment variables).

2.  **Initialize Terraform**:
    Navigate to the module directory and run:
    ```bash
    terraform init
    ```

3.  **Plan the Deployment**:
    Review the changes Terraform will make:
    ```bash
    terraform plan
    ```

4.  **Apply the Configuration**:
    Deploy the ephemeral message drop instance:
    ```bash
    terraform apply
    ```
    You will be prompted to confirm the deployment. Type `yes`.

5.  **Access the Message Drop**:
    After `terraform apply` completes, the `public_ip` and `public_dns` outputs will provide the address to access your message. Open a web browser and navigate to `http://<public_ip>` or `http://<public_dns>`.

6.  **Destroy the Instance (Optional, as it self-destructs)**:
    If you wish to terminate the instance before its scheduled self-destruction, run:
    ```bash
    terraform destroy
    ```
    You will be prompted to confirm the destruction. Type `yes`.

## Inputs

| Name                      | Description                                                               | Type     | Default                                                               | Required |
| :------------------------ | :------------------------------------------------------------------------ | :------- | :-------------------------------------------------------------------- | :------- |
| `aws_region`              | The AWS region to deploy resources in.                                    | `string` | `"us-east-1"`                                                       | no       |
| `ami_id`                  | The AMI ID for the EC2 instance (e.g., Ubuntu 22.04 LTS).                 | `string` | `"ami-053b0d53c279acc90"` (Ubuntu Server 22.04 LTS, us-east-1)      | no       |
| `instance_type`           | The EC2 instance type.                                                    | `string` | `"t2.micro"`                                                        | no       |
| `message_content`         | The message content to display on the web server.                         | `string` | `"Greetings from the ApocalypsAI! This message will self-destruct."` | no       |
| `self_destruct_minutes`   | Number of minutes until the instance automatically shuts down.            | `number` | `60` (1 hour)                                                         | no       |
| `key_pair_name`           | Optional: The name of an existing EC2 Key Pair to allow SSH access.       | `string` | `""` (no key pair by default)                                       | no       |

## Outputs

| Name                       | Description                                         |
| :------------------------- | :-------------------------------------------------- |
| `public_ip`                | The public IP address of the message drop instance. |
| `public_dns`               | The public DNS name of the message drop instance.   |
| `user_data_script_content` | The generated user_data script content (sensitive). |
