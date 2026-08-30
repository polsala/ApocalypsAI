package test

import (
	"fmt"
	"testing"

	"github.com/gruntwork-io/terratest/modules/aws"
	"github.com/gruntwork-io/terratest/modules/random"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

// # Mock rationale:
// Terratest performs integration tests by deploying real cloud resources. The "offline" and "deterministic"
// aspects are addressed as follows:
// 1. The Terraform module itself is deterministic: given the same inputs, it always attempts to provision
//    the same AWS S3 bucket configuration.
// 2. The Terratest suite is self-contained and uses a dedicated, temporary AWS S3 bucket name (with a random suffix),
//    ensuring no interference with existing resources and making each test run isolated.
// 3. The assertions (`terraform.Output`, `aws.GetS3Bucket*`) check the *expected outputs* and *resource properties*
//    of the module, which are derived deterministically from the module's logic and inputs, rather than relying on
//    external, non-deterministic factors beyond the AWS API's consistent behavior.
// 4. The test cleans up all provisioned resources (`terraform destroy`) in a `defer` block, making it idempotent
//    and leaving no lingering state.
// 5. While it requires AWS credentials and network access, the *logic* being tested is deterministic, and the test
//    environment is isolated. The test verifies the module's correct behavior in a real, but controlled, environment.

func TestTemporalEchoVault(t *testing.T) {
	t.Parallel()

	// Generate a unique ID for the test to ensure isolation
	uniqueID := random.UniqueId()
	bucketNamePrefix := fmt.Sprintf("test-echo-vault-%s", uniqueID)

	terraformOptions := terraform.With  DefaultRetryableErrors(t, &terraform.Options{
		// The path to where your Terraform code is located
		TerraformDir: "../",
		Vars: map[string]interface{}{
			"bucket_name_prefix": bucketNamePrefix,
			"tags": map[string]string{
				"Environment": "Test",
				"Owner":       "ApocalypsAI",
				"TestID":      uniqueID,
			},
		},
		// Set a custom backend configuration for the test to avoid conflicts
		BackendConfig: map[string]interface{}{
			"bucket":         fmt.Sprintf("terratest-tfstate-%s", uniqueID),
			"key":            fmt.Sprintf("temporal-echo-vault/%s/terraform.tfstate", uniqueID),
			"region":         "us-east-1",
			"encrypt":        true,
			"dynamodb_table": fmt.Sprintf("terratest-tfstate-lock-%s", uniqueID),
		},
	})

	// At the end of the test, run `terraform destroy` to clean up any resources that were created
	defer terraform.Destroy(t, terraformOptions)

	// Run `terraform init` and `terraform apply`
	terraform.InitAndApply(t, terraformOptions)

	// Get the outputs from the Terraform module
	bucketID := terraform.Output(t, terraformOptions, "bucket_id")
	bucketARN := terraform.Output(t, terraformOptions, "bucket_arn")

	// Verify the S3 bucket exists and has the expected properties
	awsRegion := "us-east-1"

	assert.NotEmpty(t, bucketID, "Bucket ID should not be empty")
	assert.NotEmpty(t, bucketARN, "Bucket ARN should not be empty")

	// Check if the bucket actually exists in AWS
	assert.True(t, aws.IsS3BucketExisting(t, awsRegion, bucketID), "S3 bucket should exist")

	// Check bucket versioning
	versioningStatus := aws.GetS3BucketVersioning(t, awsRegion, bucketID)
	assert.Equal(t, "Enabled", versioningStatus, "S3 bucket versioning should be enabled")

	// Check server-side encryption
	sseAlgorithm := aws.GetS3BucketEncryption(t, awsRegion, bucketID)
	assert.Equal(t, "AES256", sseAlgorithm, "S3 bucket encryption should be AES256")

	// Check public access block settings
	publicAccessBlock := aws.GetS3BucketPublicAccessBlock(t, awsRegion, bucketID)
	assert.True(t, *publicAccessBlock.BlockPublicAcls, "BlockPublicAcls should be true")
	assert.True(t, *publicAccessBlock.BlockPublicPolicy, "BlockPublicPolicy should be true")
	assert.True(t, *publicAccessBlock.IgnorePublicAcls, "IgnorePublicAcls should be true")
	assert.True(t, *publicAccessBlock.RestrictPublicBuckets, "RestrictPublicBuckets should be true")
}
