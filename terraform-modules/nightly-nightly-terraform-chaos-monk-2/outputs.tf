output "chaos_summary" {
  description = "Summary of chaos actions"
  value = {
    enabled     = var.enabled
    intensity   = var.intensity
    safe_mode   = var.safe_mode
    cloud_provider = var.cloud_provider
    region      = var.region
    resources   = var.resources
    chaos_count = var.enabled ? length(var.resources) : 0
  }
}

output "actions_taken" {
  description = "List of actions that would be taken"
  value = [
    for i, resource in var.resources : {
      resource  = resource
      action    = var.safe_mode ? "log" : "destroy"
      intensity = var.intensity
    }
  ]
}

output "next_chaos_window" {
  description = "When the next chaos event will occur"
  value       = "Random - check logs for details"
}
