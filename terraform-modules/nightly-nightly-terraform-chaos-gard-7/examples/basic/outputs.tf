# Basic example outputs
output "example_info" {
  description = "Information about the chaos garden example"
  value = {
    region = var.aws_region
    environment = var.environment
    chaos_duration = var.chaos_duration
    whimsy_level = var.whimsy_level
    chaos_garden_name = var.chaos_garden_name
  }
}

output "module_outputs" {
  description = "Outputs from the chaos garden module"
  value = {
    cluster_id = module.chaos_garden.chaos_cluster_id
    service_name = module.chaos_garden.chaos_service_name
    task_definition = module.chaos_garden.chaos_task_definition
    log_group = module.chaos_garden.chaos_log_group
    notifications_topic = module.chaos_garden.chaos_notifications_topic
  }
}

output "chaos_configuration" {
  description = "Chaos configuration from the module"
  value = module.chaos_garden.chaos_configuration
}
