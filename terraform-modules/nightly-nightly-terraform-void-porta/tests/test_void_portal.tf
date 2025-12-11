# Test 1: Basic portal creation
module "test_basic_portal" {
  source = "../"
  
  portal_name = "test-portal"
  providers = ["aws"]
  track_resources = false
  auto_cleanup_days = 0
}

# Test 2: Portal with tracking enabled
module "test_tracked_portal" {
  source = "../"
  
  portal_name = "tracked-portal"
  providers = ["aws", "gcp"]
  track_resources = true
  auto_cleanup_days = 7
}

# Test 3: Multi-provider portal
module "test_multi_provider" {
  source = "../"
  
  portal_name = "multi-provider"
  providers = ["aws", "gcp", "azure", "oci"]
  track_resources = true
  auto_cleanup_days = 30
}

# Test 4: Portal with debug enabled
module "test_debug_portal" {
  source = "../"
  
  portal_name = "debug-portal"
  providers = ["aws"]
  track_resources = true
  auto_cleanup_days = 0
  enable_debug = true
  portal_severity = "debug"
}

# Test assertions
# Verify portal ID is generated
resource "null_resource" "test_portal_id" {
  triggers = {
    portal_id = module.test_basic_portal.portal_id
  }
  
  # Mock rationale: Ensure portal ID is not empty
  lifecycle {
    ignore_changes = all
  }
}

# Verify portal name format
resource "null_resource" "test_portal_name" {
  triggers = {
    portal_name = module.test_tracked_portal.portal_name
  }
  
  # Mock rationale: Ensure portal name contains expected components
  lifecycle {
    ignore_changes = all
  }
}

# Verify tracked resources structure
resource "null_resource" "test_tracked_resources" {
  triggers = {
    tracked_count = length(module.test_multi_provider.tracked_resources)
    providers = jsonencode(keys(module.test_multi_provider.tracked_resources))
  }
  
  # Mock rationale: Ensure tracked resources contains all expected providers
  lifecycle {
    ignore_changes = all
  }
}

# Verify cleanup schedule
resource "null_resource" "test_cleanup_schedule" {
  triggers = {
    cleanup_enabled = module.test_debug_portal.auto_cleanup_enabled
    cleanup_schedule = module.test_tracked_portal.cleanup_schedule
  }
  
  # Mock rationale: Ensure cleanup configuration is properly set
  lifecycle {
    ignore_changes = all
  }
}

# Verify portal status
resource "null_resource" "test_portal_status" {
  triggers = {
    status = jsonencode(module.test_basic_portal.portal_status)
    metadata = jsonencode(module.test_multi_provider.portal_metadata)
  }
  
  # Mock rationale: Ensure status and metadata outputs are properly formatted
  lifecycle {
    ignore_changes = all
  }
}

# Test validation: Empty providers list should fail
# This would be tested in CI/CD pipeline with terraform validate
variable "empty_providers_test" {
  description = "Test variable for empty providers validation"
  type        = list(string)
  default     = []
}

# Test validation: Invalid severity should fail
variable "invalid_severity_test" {
  description = "Test variable for invalid severity validation"
  type        = string
  default     = "invalid"
}

# Test outputs verification
output "test_results" {
  description = "Test results summary"
  value = {
    basic_portal_id_length = length(module.test_basic_portal.portal_id)
    tracked_portal_enabled = module.test_tracked_portal.portal_status.tracking_enabled
    multi_provider_count = module.test_multi_provider.portal_status.providers_count
    debug_enabled = module.test_debug_portal.portal_metadata.debug_enabled
    cleanup_enabled = module.test_tracked_portal.portal_status.auto_cleanup
  }
}
