# Nightly Temporal Outpost Provisioner

This utility provisions a temporary, ephemeral cloud outpost, perfect for quick experiments, isolated testing, or hosting a fleeting message from the void. It's designed to be a "temporal anomaly" in your infrastructure, appearing when needed and providing clear instructions for its eventual disappearance.

## Features

*   **Ephemeral EC2 Instance:** Deploys a single AWS EC2 instance.
*   **Configurable Duration:** While the outpost doesn't self-destruct automatically, it provides a clear "self-destruct sequence" (a `terraform destroy` command) and a reminder based on a configurable duration.
*   **Whimsical Utility:** Embrace the temporary nature of existence with infrastructure that's meant to vanish.

## Prerequisites

*   [Terraform](https://www.terraform.io/downloads.html) installed.
*   AWS CLI configured with credentials that have permissions to create EC2 instances, security groups, and key pairs.

## Usage

1.  **Navigate to the utility directory:**
    ```bash
    cd terraform-modules/nightly-temporal-outpost-prov/src
    ```

2.  **Initialize Terraform:**
    ```bash
    terraform init
    ```

3.  **Review the plan (optional but recommended):**
    This will show you what resources Terraform will create.
    ```bash
    terraform plan
    ```
    You can override variables:
    ```bash
    terraform plan -var="instance_type=t3.small" -var="self_destruct_after_minutes=120"
    ```

4.  **Apply the configuration:**
    ```bash
    terraform apply
    ```
    Confirm with `yes` when prompted.

5.  **Retrieve Outpost Details:**
    After `terraform apply` completes, the outputs will display the public IP of your outpost, its instance ID, and the crucial "self-destruct sequence" command.

    ```
    Outputs:

    destroy_command = "To initiate the temporal outpost's self-destruct sequence, run: terraform destroy -auto-approve"
    instance_id = "i-0123456789abcdef0"
    public_ip = "3.8.123.45"
    ```

6.  **Initiate Self-Destruct Sequence:**
    When your temporal mission is complete, execute the `destroy_command` provided in the outputs to dismantle the outpost.

    ```bash
    terraform destroy -auto-approve
    ```

## Configuration Variables

You can customize the outpost by setting these variables:

*   `region` (string, default: `"us-east-1"`): The AWS region to deploy the outpost.
*   `instance_type` (string, default: `"t2.micro"`): The EC2 instance type.
*   `ami` (string, default: `"ami-0abcdef1234567890"`): The AMI ID for the EC2 instance. **IMPORTANT:** Replace this with a valid AMI for your chosen region and architecture (e.g., Amazon Linux 2 or Ubuntu). The default is a placeholder.
*   `outpost_name` (string, default: `"temporal-outpost"`): A name tag for your EC2 instance.
*   `self_destruct_after_minutes` (number, default: `60`): The suggested duration (in minutes) after which the outpost should be dismantled. This is for informational purposes in the output message.

## Testing

To run the automated tests, navigate to the utility's root directory and execute the test script:

```bash
cd terraform-modules/nightly-temporal-outpost-prov
./tests/test_plan.sh
```

The tests perform a `terraform plan` in a mocked environment to ensure the configuration is valid and produces the expected resources and outputs without requiring actual AWS credentials.
