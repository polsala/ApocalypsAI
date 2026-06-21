# Test Plan for Nightly Cloud Sanctuary Beacon Terraform Module

This document outlines the testing strategy for the `nightly-cloud-sanctuary-beacon` Terraform module. Due to the nature of Terraform, "unit tests" in the traditional sense (like for application code) are not directly applicable. Instead, we focus on validation of the configuration syntax and structure, and a dry-run plan to ensure the expected resources would be created.

## Testing Objectives

*   Verify that the Terraform configuration is syntactically correct and valid.
*   Ensure that the `terraform plan` command generates the expected set of AWS resources without errors.
*   Confirm that the module is self-contained and runnable.

## Prerequisites for Testing

*   Terraform CLI installed (v1.0+).
*   An internet connection to download AWS provider plugins during `terraform init`.
*   (Optional, for full integration test) AWS credentials configured, though `terraform validate` and `terraform plan` can often run without active credentials if no remote state or data sources requiring authentication are used. For this module, `terraform plan` will require credentials to fetch AWS provider schema and validate against it, but it will not create resources.

## Test Steps

1.  **Navigate to the module directory**:
    ```bash
    cd src
    ```

2.  **Initialize Terraform**:
    This step downloads the necessary AWS provider plugins and initializes the backend.
    ```bash
    terraform init
    ```
    **Expected Outcome**: The command should complete successfully, indicating that Terraform has been initialized and the AWS provider is ready. Output should include "Terraform has been successfully initialized!".

    # Mock rationale:
    # `terraform init` downloads provider binaries and sets up the working directory.
    # This is a deterministic, offline-capable step once providers are cached,
    # and its success indicates basic module structure validity.

3.  **Validate Terraform Configuration**:
    This step checks the syntax and internal consistency of the Terraform configuration files.
    ```bash
    terraform validate
    ```
    **Expected Outcome**: The command should report "The configuration is valid." Any errors indicate syntax issues or misconfigurations.

    # Mock rationale:
    # `terraform validate` performs static analysis of the HCL code.
    # It does not require AWS credentials or network calls beyond initial provider schema loading (which is part of `init`).
    # This is a deterministic and offline check for syntax correctness.

4.  **Generate a Terraform Plan (Dry Run)**:
    This step creates an execution plan, showing what actions Terraform would take if applied.
    ```bash
    terraform plan -out=tfplan
    ```
    **Expected Outcome**:
    *   The command should complete without errors.
    *   The plan should indicate the creation of approximately 6 resources (1 S3 bucket, 1 S3 public access block, 1 S3 bucket policy, 1 CloudFront OAC, 1 CloudFront distribution, 1 S3 bucket object). The exact number might vary slightly with provider versions or implicit resources.
    *   Look for lines similar to: `Plan: 6 to add, 0 to change, 0 to destroy.`
    *   The plan output should detail the properties of the resources to be created, matching the intent (e.g., S3 bucket name, CloudFront default root object, OAC configuration).

    # Mock rationale:
    # `terraform plan` generates a blueprint of changes without applying them.
    # By saving the plan to a file (`-out=tfplan`), we create a deterministic artifact.
    # The inspection of this plan file (or its console output) confirms the module's intended behavior
    # without requiring actual cloud resource provisioning, making it "offline" in terms of resource creation.
    # While it does interact with the AWS provider to fetch schema, it doesn't modify state.
    # For a truly offline test, one would mock the AWS provider, which is beyond the scope of a simple `test_plan.md`.
    # This approach validates the module's logic and resource definitions.

## Conclusion

By successfully executing `terraform init`, `terraform validate`, and `terraform plan`, we can confidently assert that the `nightly-cloud-sanctuary-beacon` module is correctly structured, syntactically valid, and capable of generating the intended infrastructure plan.
