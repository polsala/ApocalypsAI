variable "raw_ec2_instances_json" {
  description = "JSON string of EC2 instances, e.g., from 'aws ec2 describe-instances --query \"Reservations[*].Instances[*][]\"'"
  type        = string
  default     = "[]"
}

locals {
  ec2_instances = jsondecode(var.raw_ec2_instances_json)

  # Filter for stopped instances
  stopped_instances = [
    for instance in local.ec2_instances : instance
    if lookup(instance.State, "Name", "") == "stopped"
  ]
}

resource "local_file" "scavenger_report" {
  content  = templatefile("${path.module}/templates/scavenger_report.tpl", {
    stopped_instances = local.stopped_instances
    report_date       = formatdate("YYYY-MM-DD HH:mm ZZZ", timestamp())
  })
  filename = "scavenger_report.md"
}
