module "test_replicator" {
  source = "../src"

  resource_type  = "test_beacon"
  resource_count = 2
}

output "test_output_ids" {
  value = module.test_replicator.replicated_resource_ids
}
