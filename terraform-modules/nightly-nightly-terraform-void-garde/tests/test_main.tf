module "test_garden" {
  source = "../"

  garden_name        = "test-void-garden"
  environment        = "test"
  max_instances      = 2
  min_instances      = 1
  desired_capacity   = 1
  easter_egg_path    = "/test-easter-egg"
  key_name           = ""
  region             = "us-east-1"
}

# Test that the garden URL is not empty
output "test_garden_url" {
  value = module.test_garden.garden_url
}

# Test that the easter egg path is correct
output "test_easter_egg_path" {
  value = module.test_garden.easter_egg_path
}
