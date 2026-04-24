# Mock rationale: These outputs are for the test configuration to ensure the module's outputs are correctly exposed.
output "test_bucket_id" {
  value = module.test_scavenger_cache.bucket_id
}

output "test_bucket_arn" {
  value = module.test_scavenger_cache.bucket_arn
}

output "test_bucket_domain_name" {
  value = module.test_scavenger_cache.bucket_domain_name
}
