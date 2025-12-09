# Test outputs
output "test_chaos_schedule" {
  description = "Test chaos schedule output"
  value       = module.chaos_orchestrator.chaos_schedule
}

output "test_resource_ttl" {
  description = "Test resource TTL output"
  value       = module.chaos_orchestrator.resource_ttl
}

output "test_max_resources" {
  description = "Test maximum resources output"
  value       = module.chaos_orchestrator.max_resources
}

output "test_providers" {
  description = "Test providers output"
  value       = module.chaos_orchestrator.providers
}

output "test_chaos_enabled" {
  description = "Test chaos enabled status"
  value       = module.chaos_orchestrator.chaos_enabled
}

output "test_resource_types" {
  description = "Test resource types"
  value       = module.chaos_orchestrator.resource_types
}
