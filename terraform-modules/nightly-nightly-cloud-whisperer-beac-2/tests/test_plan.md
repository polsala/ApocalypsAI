# Test Plan for Nightly Cloud-Whisperer Beacon

This document outlines the testing procedure for the `nightly-cloud-whisperer-beacon` Terraform module. Since Terraform modules define infrastructure, traditional unit tests with mocks are not directly applicable in the same way as application code. Instead, we focus on syntax validation and plan verification.

## Prerequisites

*   Terraform CLI installed (version 1.0.0 or higher recommended).
*   AWS CLI configured with credentials (for `terraform init` to download provider, though `validate` and `plan` can run offline after init).

## Offline Test: Syntax and Configuration Validation

This test ensures that the Terraform configuration files are syntactically correct and internally consistent, without requiring any interaction with the AWS API beyond initial provider download.

1.  **Navigate to the module directory:**
    ```bash
    cd src
    ```

2.  **Initialize Terraform (if not already done):**
    This step downloads the necessary AWS provider. It requires network access but does not create any AWS resources. Once initialized, subsequent `validate` and `plan` commands can run offline.
    ```bash
    terraform init
    ```
    # Mock rationale: `terraform init` downloads provider plugins. For offline testing, assume this step has been completed once. The actual validation and planning steps do not require live API calls after initialization.

3.  **Validate the Terraform configuration:**
    ```bash
    terraform validate
    ```

    **Expected Outcome:**
    The command should exit with a zero status code and output:
    ```
    Success! The configuration is valid.
    ```
    Any errors indicate syntax issues, missing variables, or invalid resource configurations. This test is fully deterministic and offline once `terraform init` has completed its initial provider download.

## Offline Test: Plan Verification (Conceptual)

While `terraform plan` typically interacts with a remote state and cloud provider to determine changes, it can be run "offline" in the sense that it doesn't *apply* changes. The output of `terraform plan` can be inspected to ensure the module intends to create the expected resources.

1.  **Navigate to the module directory:**
    ```bash
    cd src
    ```

2.  **Generate a Terraform plan:**
    You might need to provide values for variables if they don't have defaults or if you want to override them. For this module, `content_bucket_name` has a default, but it's highly recommended to override it with a unique name.
    ```bash
    terraform plan -var="content_bucket_name=my-unique-beacon-bucket-12345"
    ```
    # Mock rationale: `terraform plan` output is a prediction. For offline testing, we verify the *structure* and *types* of resources it *intends* to create, rather than live state. The `-var` flag allows deterministic input.

    **Expected Outcome (High-Level):**
    The plan output should indicate that the following resources will be added:
    *   `aws_s3_bucket.content_bucket` (1 to be added)
    *   `aws_s3_bucket_public_access_block.content_bucket_public_access_block` (1 to be added)
    *   `aws_s3_bucket_ownership_controls.content_bucket_ownership_controls` (1 to be added)
    *   `aws_s3_bucket_acl.content_bucket_acl` (1 to be added)
    *   `aws_s3_bucket_website_configuration.content_bucket_website_config` (1 to be added)
    *   `aws_cloudfront_origin_access_identity.oai` (1 to be added)
    *   `aws_s3_bucket_policy.content_bucket_policy` (1 to be added)
    *   `aws_cloudfront_distribution.s3_distribution` (1 to be added)
    *   `aws_s3_object.index_html` (1 to be added)
    *   `aws_s3_object.error_html` (1 to be added)

    The plan should show `Plan: 10 to add, 0 to change, 0 to destroy.` (or similar, depending on exact resource count).
    This verification is "offline" in the sense that it doesn't modify any cloud resources, and its output, given consistent input variables, is predictable for a fresh deployment.

## Integration Test (Manual / Out-of-Scope for Offline Tests)

For a complete verification, one would typically run `terraform apply`, then use `curl` or a web browser to access the `cloudfront_domain_name` output and verify the content. This is an integration test and requires live AWS resources, thus it's not part of the deterministic, offline test suite.
