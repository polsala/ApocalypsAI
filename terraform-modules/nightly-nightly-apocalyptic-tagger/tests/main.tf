# This configuration tests the 'nightly-apocalyptic-tagger' module.
# It uses a mock AWS provider to ensure tests are deterministic and offline.

module "test_tagger_dev_instance" {
  source = "../src" # Path to the module under test
  
  resource_name_prefix = "sentry"
  resource_type        = "EC2-Instance"
  environment          = "dev"
}

module "test_tagger_prod_db" {
  source = "../src" # Path to the module under test
  
  resource_name_prefix = "data-vault"
  resource_type        = "RDS-DB"
  environment          = "prod"
}

output "dev_instance_name" {
  value = module.test_tagger_dev_instance.generated_name
}

output "dev_instance_tags" {
  value = module.test_tagger_dev_instance.generated_tags
}

output "prod_db_name" {
  value = module.test_tagger_prod_db.generated_name
}

output "prod_db_tags" {
  value = module.test_tagger_prod_db.generated_tags
}
