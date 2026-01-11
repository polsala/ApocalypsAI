# Mock rationale: This file is used by the test script to instantiate the module
# with dummy values for offline `terraform validate`. It does not deploy resources.

module "echo_chamber_test" {
  source = "./src" # Points to the module source copied by the test script
  
  region               = "us-east-1"
  bucket_name_prefix   = "test-apocalypsai-echo"
  enable_lambda_echo   = true
  tags = {
    Project     = "ApocalypsAI-Test"
    Environment = "Test"
  }
}

module "echo_chamber_no_lambda_test" {
  source = "./src"
  
  region               = "us-west-2"
  bucket_name_prefix   = "test-apocalypsai-no-lambda"
  enable_lambda_echo   = false
  tags = {
    Project     = "ApocalypsAI-Test"
    Environment = "Test"
  }
}
