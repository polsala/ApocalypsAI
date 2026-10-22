output "safehouse_path" {
  description = "Absolute path to the safe‑house directory"
  value       = "${path.module}/${var.safehouse_name}"
}
