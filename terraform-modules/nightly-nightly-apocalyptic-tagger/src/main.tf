locals {
  apocalypse_themes = [
    "Wasteland-Wanderer",
    "Temporal-Rift-Monitor",
    "Void-Whisperer",
    "Shelter-Sentry",
    "Resource-Scavenger",
    "Anomaly-Tracker",
    "Echo-Chamber-Node",
    "Chronos-Beacon"
  ]
  
  # Deterministically pick a theme based on the length of the prefix
  # Mock rationale: This uses a simple, deterministic algorithm to select a theme
  # based on input length, ensuring consistent results without external calls.
  random_theme = element(local.apocalypse_themes, abs(length(var.resource_name_prefix) % length(local.apocalypse_themes)))
  
  generated_name_base = "${var.resource_name_prefix}-${local.random_theme}-${var.environment}"
  
  # Ensure the name is within typical AWS tag value limits (256 chars)
  generated_name = substr(local.generated_name_base, 0, min(length(local.generated_name_base), 255))

  common_tags = {
    "Project"         = "ApocalypsAI-Community"
    "ManagedBy"       = "ApocalypsAI-Integrator"
    "ApocalypsePhase" = "Post-Collapse-Rebuild"
    "Squad"           = "Nightly-Integrators"
    "Purpose"         = var.resource_type
    "Environment"     = var.environment
  }
}

output "generated_name" {
  description = "The whimsically generated name for the resource."
  value       = local.generated_name
}

output "generated_tags" {
  description = "A map of apocalypse-themed tags for the resource."
  value       = local.common_tags
}
