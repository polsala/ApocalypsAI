output "test_summary" {
  description = "Summary of test results"
  value = {
    test_passed = (
      contains(split("-", module.chaos_garden_test.garden_summary.bucket_name), "test-chaos-garden") &&
      contains(split("-", module.chaos_garden_test.garden_summary.lambda_name), "test-chaos-garden") &&
      module.chaos_garden_test.garden_summary.chaos_level == 2 &&
      module.chaos_garden_test.garden_summary.chaos_enabled == true
    )
    bucket_name = module.chaos_garden_test.garden_summary.bucket_name
    lambda_name = module.chaos_garden_test.garden_summary.lambda_name
    chaos_level = module.chaos_garden_test.garden_summary.chaos_level
    chaos_enabled = module.chaos_garden_test.garden_summary.chaos_enabled
  }
}
