locals {
  # Sanitize names for use in prefixes (lowercase, replace spaces/special chars with hyphens)
  sanitized_constellation_name = lower(replace(var.constellation_name, "/[^a-zA-Z0-9]+/", "-"))
  sanitized_environment        = lower(replace(var.environment, "/[^a-zA-Z0-9]+/", "-"))
  
  # Generate a consistent prefix
  generated_prefix = "${local.sanitized_constellation_name}-${local.sanitized_environment}"

  # Define base tags
  base_tags = {
    "Constellation" = var.constellation_name
    "Environment"   = var.environment
    "ManagedBy"     = "ApocalypsAI-ConstellationMapper"
  }

  # Merge base tags with additional tags
  merged_tags = merge(local.base_tags, var.additional_tags)
}
