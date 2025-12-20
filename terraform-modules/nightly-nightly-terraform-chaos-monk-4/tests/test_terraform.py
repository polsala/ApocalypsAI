package test

import (
	"fmt"
	"strings"
	"testing"
	"time"

	"github.com/gruntwork-io/terratest/modules/aws"
	"github.com/gruntwork-io/terratest/modules/random"
	"github.com/gruntwork-io/terratest/modules/terraform"
	test_structure "github.com/gruntwork-io/terratest/modules/test-structure"
	"github.com/stretchr/testify/assert"
)

func TestTerraformChaosMonkeyBasic(t *testing.T) {
	t.Parallel()

	// Define the test stages
	test_structure.RunTestStage(t, "setup", func() {
		terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
			TerraformDir: "../examples/basic-usage",
			Vars: map[string]interface{}{
				"chaos_level": "gentle",
				"enabled":     true,
				"dry_run":     true,
				"target_instances": []string{
					"i-0123456789abcdef0",
					"i-0987654321fedcba0",
				},
				"minimum_instance_count": 1,
				"chaos_schedule":         "cron(0/30 * * * ? *)",
				"notification_email":     "test@example.com",
				"included_tags": map[string]string{
					"Environment": "test",
					"Team":        "platform",
				},
				"excluded_tags": map[string]string{
					"Critical": "true",
				},
			},
			EnvVars: map[string]string{
				"AWS_DEFAULT_REGION": "us-east-1",
			},
		})

		defer test_structure.RunTestStage(t, "teardown", func() {
			terraform.Destroy(t, terraformOptions)
		})

		test_structure.RunTestStage(t, "validate", func() {
			terraform.InitAndApply(t, terraformOptions)

			// Verify outputs
			chaosEnabled := terraform.Output(t, terraformOptions, "chaos_enabled")
			assert.Equal(t, "true", chaosEnabled)

			chaosLevel := terraform.Output(t, terraformOptions, "chaos_level")
			assert.Equal(t, "gentle", chaosLevel)

			chaosSchedule := terraform.Output(t, terraformOptions, "chaos_schedule")
			assert.Equal(t, "cron(0/30 * * * ? *)", chaosSchedule)

			targetCount := terraform.Output(t, terraformOptions, "target_instance_count")
			assert.Equal(t, "2", targetCount)

			dryRunMode := terraform.Output(t, terraformOptions, "dry_run_mode")
			assert.Equal(t, "true", dryRunMode)

			// Verify Lambda function exists
			lambdaFunctionName := terraform.Output(t, terraformOptions, "lambda_function_name")
			assert.NotEmpty(t, lambdaFunctionName)

			// Verify CloudWatch Log Group exists
			logGroupName := terraform.Output(t, terraformOptions, "log_group_name")
			assert.Equal(t, "/apocalypsaid/chaos-monkey", logGroupName)

			// Verify EventBridge rule exists
			eventRuleName := terraform.Output(t, terraformOptions, "event_rule_name")
			assert.NotEmpty(t, eventRuleName)

			// Verify IAM role and policy exist
			lambdaRoleName := terraform.Output(t, terraformOptions, "lambda_function_name") + "-role"
			aws.GetIamRoleArn(t, "us-east-1", lambdaRoleName)
		})
	})
}

func TestTerraformChaosMonkeyAdvanced(t *testing.T) {
	t.Parallel()

	test_structure.RunTestStage(t, "setup", func() {
		uniqueID := random.UniqueId()
		terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
			TerraformDir: "../examples/advanced-usage",
			Vars: map[string]interface{}{
				"chaos_level": "extreme",
				"enabled":     true,
				"dry_run":     false,
				"target_instances": []string{
					"i-0123456789abcdef0",
					"i-0987654321fedcba0",
					"i-11111111111111111",
					"i-22222222222222222",
					"i-33333333333333333",
				},
				"minimum_instance_count": 3,
				"circuit_breaker_threshold": 5,
				"chaos_schedule":         "cron(0/15 9-17 ? * MON-FRI *)",
				"maintenance_windows": []string{
					"cron(0 2 ? * *)",
					"cron(0 0 ? * SUN *)",
				},
				"chaos_types": []string{
					"instance_termination",
					"instance_stop",
					"network_latency",
					"cpu_stress",
					"memory_stress",
					"disk_io_stress",
				},
				"notification_email": "platform-team@example.com",
				"verbose_logging":    true,
				"included_tags": map[string]string{
					"Environment": "production",
					"Team":        "platform",
					"ChaosReady":  "true",
				},
				"excluded_tags": map[string]string{
					"Critical":       "true",
					"Database":       "true",
					"LoadBalancer":   "true",
				},
			},
			EnvVars: map[string]string{
				"AWS_DEFAULT_REGION": "us-east-1",
			},
		})

		defer test_structure.RunTestStage(t, "teardown", func() {
			terraform.Destroy(t, terraformOptions)
		})

		test_structure.RunTestStage(t, "validate", func() {
			terraform.InitAndApply(t, terraformOptions)

			// Verify advanced configuration outputs
			chaosLevel := terraform.Output(t, terraformOptions, "aws_chaos_status")
			assert.Contains(t, chaosLevel, "enabled": true)

			targetCount := terraform.Output(t, terraformOptions, "aws_target_count")
			assert.Equal(t, "5", targetCount)

			chaosSchedule := terraform.Output(t, terraformOptions, "aws_chaos_schedule")
			assert.Equal(t, "cron(0/15 9-17 ? * MON-FRI *)", chaosSchedule)

			// Verify Lambda function has correct environment variables
			lambdaFunctionName := terraform.Output(t, terraformOptions, "aws_chaos_lambda")
			lambdaConfig := aws.GetLambdaFunction(t, "us-east-1", lambdaFunctionName)
			
			// Check environment variables
			envVars := lambdaConfig.Configuration.Environment.Variables
			assert.Equal(t, "extreme", *envVars["CHAOS_LEVEL"])
			assert.Equal(t, "false", *envVars["DRY_RUN"])
			assert.Equal(t, "3", *envVars["MIN_INSTANCE_COUNT"])
		})
	})
}

func TestTerraformChaosMonkeyDisabled(t *testing.T) {
	t.Parallel()

	test_structure.RunTestStage(t, "setup", func() {
		terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
			TerraformDir: "../examples/basic-usage",
			Vars: map[string]interface{}{
				"chaos_level": "medium",
				"enabled":     false,
				"dry_run":     true,
				"target_instances": []string{
					"i-0123456789abcdef0",
				},
				"minimum_instance_count": 1,
				"chaos_schedule":         "cron(0/30 * * * ? *)",
			},
			EnvVars: map[string]string{
				"AWS_DEFAULT_REGION": "us-east-1",
			},
		})

		defer test_structure.RunTestStage(t, "teardown", func() {
			terraform.Destroy(t, terraformOptions)
		})

		test_structure.RunTestStage(t, "validate", func() {
			terraform.InitAndApply(t, terraformOptions)

			// Verify chaos is disabled
			chaosEnabled := terraform.Output(t, terraformOptions, "chaos_enabled")
			assert.Equal(t, "false", chaosEnabled)

			// Verify EventBridge rule is not created when disabled
			eventRuleName := terraform.Output(t, terraformOptions, "event_rule_name")
			assert.Equal(t, "", eventRuleName)

			// Verify Lambda function is still created (for manual triggering)
			lambdaFunctionName := terraform.Output(t, terraformOptions, "lambda_function_name")
			assert.NotEmpty(t, lambdaFunctionName)
		})
	})
}

func TestTerraformChaosMonkeyDryRun(t *testing.T) {
	t.Parallel()

	test_structure.RunTestStage(t, "setup", func() {
		terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
			TerraformDir: "../examples/basic-usage",
			Vars: map[string]interface{}{
				"chaos_level": "medium",
				"enabled":     true,
				"dry_run":     true,
				"target_instances": []string{
					"i-0123456789abcdef0",
				},
				"minimum_instance_count": 1,
				"chaos_schedule":         "cron(0/30 * * * ? *)",
			},
			EnvVars: map[string]string{
				"AWS_DEFAULT_REGION": "us-east-1",
			},
		})

		defer test_structure.RunTestStage(t, "teardown", func() {
			terraform.Destroy(t, terraformOptions)
		})

		test_structure.RunTestStage(t, "validate", func() {
			terraform.InitAndApply(t, terraformOptions)

			// Verify dry run mode is enabled
			dryRunMode := terraform.Output(t, terraformOptions, "dry_run_mode")
			assert.Equal(t, "true", dryRunMode)

			// Verify Lambda function has dry run enabled
			lambdaFunctionName := terraform.Output(t, terraformOptions, "lambda_function_name")
			lambdaConfig := aws.GetLambdaFunction(t, "us-east-1", lambdaFunctionName)
			
			envVars := lambdaConfig.Configuration.Environment.Variables
			assert.Equal(t, "true", *envVars["DRY_RUN"])
		})
	})
}

func TestTerraformChaosMonkeyTags(t *testing.T) {
	t.Parallel()

	test_structure.RunTestStage(t, "setup", func() {
		terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
			TerraformDir: "../examples/basic-usage",
			Vars: map[string]interface{}{
				"chaos_level": "medium",
				"enabled":     true,
				"dry_run":     true,
				"target_instances": []string{
					"i-0123456789abcdef0",
				},
				"minimum_instance_count": 1,
				"chaos_schedule":         "cron(0/30 * * * ? *)",
				"included_tags": map[string]string{
					"Environment": "production",
					"Team":        "platform",
				},
				"excluded_tags": map[string]string{
					"Critical": "true",
					"Database": "true",
				},
			},
			EnvVars: map[string]string{
				"AWS_DEFAULT_REGION": "us-east-1",
			},
		})

		defer test_structure.RunTestStage(t, "teardown", func() {
			terraform.Destroy(t, terraformOptions)
		})

		test_structure.RunTestStage(t, "validate", func() {
			terraform.InitAndApply(t, terraformOptions)

			// Verify tag configuration is passed correctly
			status := terraform.Output(t, terraformOptions, "chaos_status")
			assert.Contains(t, status, "enabled": true)

			// Verify Lambda function has tag configuration
			lambdaFunctionName := terraform.Output(t, terraformOptions, "lambda_function_name")
			lambdaConfig := aws.GetLambdaFunction(t, "us-east-1", lambdaFunctionName)
			
			envVars := lambdaConfig.Configuration.Environment.Variables
			assert.NotEmpty(t, *envVars["INCLUDED_TAGS"])
			assert.NotEmpty(t, *envVars["EXCLUDED_TAGS"])
		})
	})
}

// Helper function to wait for Lambda function to be ready
func waitForLambdaReady(t *testing.T, region, functionName string, timeout time.Duration) {
	start := time.Now()
	for time.Since(start) < timeout {
		_, err := aws.GetLambdaFunction(t, region, functionName)
		if err == nil {
			return
		}
		time.Sleep(10 * time.Second)
	}
	t.Fatalf("Lambda function %s not ready after %v", functionName, timeout)
}

// Helper function to invoke Lambda function for testing
func invokeLambdaForTest(t *testing.T, region, functionName string) (string, error) {
	input := `{"test": true, "dry_run": true}`
	
	result, err := aws.InvokeLambdaFunction(t, region, functionName, input)
	if err != nil {
		return "", err
	}
	
	return result, nil
}
