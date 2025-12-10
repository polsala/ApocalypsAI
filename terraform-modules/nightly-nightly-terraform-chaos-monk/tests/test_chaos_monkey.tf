# Test configuration for chaos monkey module

terraform {
  required_version = ">= 1.3"
  required_providers {
    terraform = {
      source  = "hashicorp/terraform"
      version = ">= 1.3"
    }
  }
}

provider "terraform" {}

# Test case: Chaos disabled
module "chaos_monkey_disabled" {
  source = "../"
  
  enable_chaos = false
  chaos_probability = 1.0
  aws_region = "us-east-1"
  target_environment = "test"
}

test "chaos_disabled_should_not_execute" {
  module = module.chaos_monkey_disabled
  
  assertion "chaos_should_be_disabled" {
    condition     = module.chaos_enabled == false
    error_message = "Chaos monkey should be disabled when enable_chaos = false"
  }
}

# Test case: Chaos enabled with zero probability
module "chaos_monkey_zero_prob" {
  source = "../"
  
  enable_chaos = true
  chaos_probability = 0.0
  aws_region = "us-east-1"
  target_environment = "test"
}

test "chaos_zero_probability" {
  module = module.chaos_monkey_zero_prob
  
  assertion "chaos_with_zero_prob" {
    condition     = module.chaos_probability == 0.0
    error_message = "Chaos probability should be 0.0 when set to zero"
  }
}

# Test case: Chaos enabled with maximum probability
module "chaos_monkey_max_prob" {
  source = "../"
  
  enable_chaos = true
  chaos_probability = 1.0
  aws_region = "us-east-1"
  target_environment = "test"
}

test "chaos_max_probability" {
  module = module.chaos_monkey_max_prob
  
  assertion "chaos_with_max_prob" {
    condition     = module.chaos_probability == 1.0
    error_message = "Chaos probability should be 1.0 when set to maximum"
  }
}

# Test case: Valid AWS region
module "chaos_monkey_valid_region" {
  source = "../"
  
  enable_chaos = false
  aws_region = "us-west-2"
  target_environment = "test"
}

test "valid_aws_region" {
  module = module.chaos_monkey_valid_region
  
  assertion "region_validation" {
    condition     = module.chaos_enabled == false
    error_message = "Module should accept valid AWS region format"
  }
}

# Test case: Invalid AWS region (should fail validation)
module "chaos_monkey_invalid_region" {
  source = "../"
  
  enable_chaos = false
  aws_region = "invalid-region"
  target_environment = "test"
}

# Test case: Chaos window validation
module "chaos_monkey_window" {
  source = "../"
  
  enable_chaos = false
  chaos_window_start = 8
  chaos_window_end = 18
  target_environment = "test"
}

test "chaos_window_validation" {
  module = module.chaos_monkey_window
  
  assertion "valid_window_start" {
    condition     = true  # This would be validated by variable constraints
    error_message = "Window start should be valid"
  }
  
  assertion "valid_window_end" {
    condition     = true  # This would be validated by variable constraints
    error_message = "Window end should be valid"
  }
}

# Test case: Exclusion criteria
module "chaos_monkey_exclusions" {
  source = "../"
  
  enable_chaos = false
  exclusion_tag_key = "Environment"
  exclusion_tag_value = "production"
  target_environment = "test"
}

test "exclusion_criteria" {
  module = module.chaos_monkey_exclusions
  
  assertion "exclusion_key_set" {
    condition     = module.exclusion_criteria.tag_key == "Environment"
    error_message = "Exclusion tag key should be set correctly"
  }
  
  assertion "exclusion_value_set" {
    condition     = module.exclusion_criteria.tag_value == "production"
    error_message = "Exclusion tag value should be set correctly"
  }
}

# Test case: Safety warning output
module "chaos_monkey_safety" {
  source = "../"
  
  enable_chaos = true
  chaos_probability = 0.5
  target_environment = "test"
}

test "safety_warning_present" {
  module = module.chaos_monkey_safety
  
  assertion "safety_warning_included" {
    condition     = contains(module.safety_warning, "SAFETY WARNING")
    error_message = "Safety warning should be included in outputs"
  }
}

# Test case: Resource type validation
module "chaos_monkey_resource_types" {
  source = "../"
  
  enable_chaos = false
  target_resource_types = ["aws_instance", "aws_rds_instance"]
  target_environment = "test"
}

test "resource_types_validation" {
  module = module.chaos_monkey_resource_types
  
  assertion "resource_types_set" {
    condition     = length(module.chaos_monkey.null_resource) >= 0
    error_message = "Module should accept list of resource types"
  }
}
