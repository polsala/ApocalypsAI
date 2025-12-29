# Mock rationale: For offline, deterministic testing, we provide a static JSON string
# that simulates the output of a cloud provider's CLI command (e.g., `aws ec2 describe-instances`).
# This allows the module's logic for parsing and reporting to be tested without
# requiring actual cloud credentials or network access.

module "scavenger_test" {
  source = "../" # Refers to the parent directory where the module is defined

  raw_ec2_instances_json = jsonencode([
    {
      "InstanceId"    = "i-0a1b2c3d4e5f6a7b8",
      "InstanceType"  = "t2.micro",
      "LaunchTime"    = "2023-01-01T12:00:00.000Z",
      "State"         = { "Code" = 80, "Name" = "stopped" },
      "Tags"          = [{ "Key" = "Name", "Value" = "ForgottenServer" }]
    },
    {
      "InstanceId"    = "i-0f1e2d3c4b5a6f7e8",
      "InstanceType"  = "m5.large",
      "LaunchTime"    = "2023-03-15T08:30:00.000Z",
      "State"         = { "Code" = 16, "Name" = "running" },
      "Tags"          = [{ "Key" = "Name", "Value" = "ActiveWorker" }]
    },
    {
      "InstanceId"    = "i-0c9b8a7f6e5d4c3b2",
      "InstanceType"  = "t3.small",
      "LaunchTime"    = "2023-02-10T10:15:00.000Z",
      "State"         = { "Code" = 80, "Name" = "stopped" },
      "Tags"          = [{ "Key" = "Name", "Value" = "OldDevBox" }]
    }
  ])
}

# Test case 1: Check if the report content is generated and contains expected stopped instances.
run "check_report_content" {
  command = "apply"

  check "report_contains_stopped_instances" {
    # Mock rationale: We assert against the module's output, which is derived from the mocked input.
    # This ensures the processing logic within the module correctly identifies and formats
    # the 'stopped' instances into the report.
    assert {
      condition     = contains(module.scavenger_test.scavenger_report_content, "| i-0a1b2c3d4e5f6a7b8 | t2.micro | 2023-01-01T12:00:00.000Z | ForgottenServer |") &&
                        contains(module.scavenger_test.scavenger_report_content, "| i-0c9b8a7f6e5d4c3b2 | t3.small | 2023-02-10T10:15:00.000Z | OldDevBox |") &&
                        !contains(module.scavenger_test.scavenger_report_content, "ActiveWorker")
      error_message = "Scavenger report did not correctly identify or format stopped instances."
    }
  }

  check "report_format_is_markdown" {
    # Mock rationale: Verifies the output format is as expected for a markdown file.
    assert {
      condition     = startswith(module.scavenger_test.scavenger_report_content, "# ApocalypsAI Cloud Scavenger Report") &&
                        contains(module.scavenger_test.scavenger_report_content, "## 🤖 Stopped EC2 Instances") &&
                        contains(module.scavenger_test.scavenger_report_content, "| Instance ID | Instance Type | Launch Time | Tags (Name) |")
      error_message = "Scavenger report format is not as expected markdown."
    }
  }
}

# Test case 2: Check behavior with no stopped instances.
module "scavenger_no_stopped_test" {
  source = "../"

  raw_ec2_instances_json = jsonencode([
    {
      "InstanceId"    = "i-0f1e2d3c4b5a6f7e8",
      "InstanceType"  = "m5.large",
      "LaunchTime"    = "2023-03-15T08:30:00.000Z",
      "State"         = { "Code" = 16, "Name" = "running" },
      "Tags"          = [{ "Key" = "Name", "Value" = "ActiveWorker" }]
    }
  ])
}

run "check_no_stopped_instances_report" {
  command = "apply"

  check "report_indicates_no_stopped_instances" {
    # Mock rationale: Ensures the report correctly states when no stopped instances are found.
    assert {
      condition     = contains(module.scavenger_no_stopped_test.scavenger_report_content, "_No stopped EC2 instances found. Your digital camp is lean and mean!_") &&
                        !contains(module.scavenger_no_stopped_test.scavenger_report_content, "| Instance ID |") # No table header
      error_message = "Report did not correctly handle the case with no stopped instances."
    }
  }
}
