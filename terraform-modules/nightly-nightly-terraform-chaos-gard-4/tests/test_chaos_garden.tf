module "chaos_garden_test" {
  source = "../"

  garden_name   = "test-chaos-garden"
  region        = "us-west-2"
  chaos_level   = 2
  enable_chaos  = true
}

# Test assertions
resource "null_resource" "test_assertions" {
  triggers = {
    bucket_name = module.chaos_garden_test.garden_summary.bucket_name
    lambda_name = module.chaos_garden_test.garden_summary.lambda_name
  }
}

# Output test results
output "test_results" {
  value = {
    bucket_contains_garden_name = contains(split("-", module.chaos_garden_test.garden_summary.bucket_name), "test-chaos-garden")
    lambda_contains_garden_name = contains(split("-", module.chaos_garden_test.garden_summary.lambda_name), "test-chaos-garden")
    chaos_level_correct         = module.chaos_garden_test.garden_summary.chaos_level == 2
    chaos_enabled               = module.chaos_garden_test.garden_summary.chaos_enabled == true
  }
}
