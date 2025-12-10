# Basic Chaos Garden Example

module "chaos_garden" {
  source = "../../"

  garden_name = "basic-chaos-garden"
  region      = "us-west-2"
  chaos_level = 3
  enable_chaos = true
}

output "basic_garden_info" {
  value = module.chaos_garden.garden_summary
}
