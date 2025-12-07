resource "null_resource" "dust_bunny_scheduler" {
  provisioner "local-exec" {
    command = "echo '🧹 Starting Digital Dust Bunny Sweep...'", "terraform apply -auto-approve"
  }

  triggers = {
    schedule = var.schedule
    retention = var.retention_days
  }
}

variable "schedule" {
  description = "Cron schedule for cleanup (e.g. '0 2 * * *')"
  type        = string
}

variable "retention_days" {
  description = "Number of days to retain resources"
  type        = number
}

output "last_cleanup" {
  value       = null_resource.dust_bunny_scheduler.id
  description = "Last successful cleanup timestamp"
}
