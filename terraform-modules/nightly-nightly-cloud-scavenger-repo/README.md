# Nightly Cloud Scavenger Report

Greetings, fellow survivor! The ApocalypsAI Nightly Integrator presents a whimsical-yet-useful utility to help you manage your precious cloud resources in the digital wasteland.

## 📜 Summary

This Terraform module acts as a digital scavenger, taking raw JSON data about your cloud resources (e.g., EC2 instances, EBS volumes, etc.) and generating a human-readable markdown report. It highlights potentially idle or underutilized assets, helping you identify 'scavengeable' resources that could be optimized or repurposed to conserve your digital energy.

Currently, it focuses on identifying `stopped` EC2 instances.

## 🛠️ How It Works

1.  **Input Data**: You provide raw JSON output from your cloud provider's CLI (e.g., `aws ec2 describe-instances`) as an input variable to the module.
2.  **Processing**: The module uses Terraform's `jsondecode` function to parse the input, then filters and processes the data using `locals` and `for_each` expressions.
3.  **Report Generation**: A markdown report is generated using Terraform's `templatefile` function, incorporating the identified 'scavengeable' resources.
4.  **Output**: The generated report content is available as a module output and also written to a local file (`scavenger_report.md`).

## 🚀 Usage

### Prerequisites

*   Terraform CLI installed.
*   Your cloud provider's CLI (e.g., AWS CLI) configured to fetch resource data.

### Step-by-Step

1.  **Fetch Raw Cloud Data**:
    Use your cloud provider's CLI to get a JSON dump of your resources. For AWS EC2 instances, you might run:
    ```bash
    aws ec2 describe-instances --query 'Reservations[*].Instances[*][]' --output json > instances.json
    ```
    Ensure the query extracts a flat list of instance objects.

2.  **Create Your Terraform Configuration**:
    Create a `main.tf` file in a new directory and call this module, passing the content of your `instances.json` file.

    ```terraform
    # main.tf
    module "cloud_scavenger" {
      source = "./path/to/nightly-cloud-scavenger-report" # Adjust this path to where you've placed the module

      raw_ec2_instances_json = file("instances.json")
    }

    output "report_content" {
      value = module.cloud_scavenger.scavenger_report_content
    }
    ```

3.  **Initialize and Apply Terraform**:
    Navigate to your new directory and run:

    ```bash
    terraform init
    terraform apply
    ```

    Terraform will show you the plan, including the creation of the `scavenger_report.md` file. Confirm the apply.

4.  **View the Report**:
    After a successful apply, a `scavenger_report.md` file will be created in your current directory. Open it to see your whimsical scavenger findings!

## 📂 Module Structure

```
nightly-cloud-scavenger-report/
├── README.md
├── main.tf
├── outputs.tf
├── templates/
│   └── scavenger_report.tpl
└── tests/
    └── main.tf
```

## ⚙️ Inputs

*   `raw_ec2_instances_json` (string, optional): A JSON string representing a list of EC2 instances. Defaults to `"[]"`.
    *   Example value: `jsonencode([ { "InstanceId": "i-123", "State": { "Name": "stopped" }, ... } ])`

## 📊 Outputs

*   `scavenger_report_content` (string): The full content of the generated markdown scavenger report.

## 🧪 Testing

To run the automated tests for this module, navigate to the `tests/` directory within the module and execute:

```bash
terraform init
terraform test
```

The tests use mock JSON data to simulate cloud provider output, ensuring the module's parsing and reporting logic works correctly offline and deterministically.
