resource "null_resource" "replicated_resource" {
  count = var.resource_count

  triggers = {
    resource_type = var.resource_type
    instance_id   = "instance-${count.index}"
    timestamp     = timestamp() # To force recreation if triggers change
  }

  provisioner "local-exec" {
    command = "echo \"Provisioning ${var.resource_type} instance ${count.index} with ID instance-${count.index}\""
  }

  provisioner "local-exec" {
    when    = destroy
    command = "echo \"Destroying ${var.resource_type} instance ${count.index} with ID instance-${count.index}\""
  }
}

output "replicated_resource_ids" {
  description = "List of IDs for the replicated resources."
  value       = [for r in null_resource.replicated_resource : r.triggers.instance_id]
}
