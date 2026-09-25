output "safehouse_name" {\n  description = "Generated safe‑house name."\n  value       = "${local.base_name}-${random_integer.suffix.result}"\n}\n
