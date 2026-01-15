variable "enabled" {
  type    = bool
  default = false
}

variable "destruction_rate" {
  type    = number
  default = 0.1
  validation {
    condition     = var.destruction_rate >= 0 && var.destruction_rate <= 1
    error_message = "Destruction rate must be between 0 and 1."
  }
}

variable "resource_tags" {
  type    = map(string)
  default = {}
}

data "aws_instances" "tagged" {
  count = var.enabled ? 1 : 0
  filter {
    name   = "tag-key"
    values = keys(var.resource_tags)
  }
}

resource "random_shuffle" "targets" {
  input        = var.enabled ? data.aws_instances.tagged[0].ids : []
  result_count = floor(length(data.aws_instances.tagged[0].ids) * var.destruction_rate)
}

resource "null_resource" "destroy_instance" {
  count = length(random_shuffle.targets.result)
  triggers = {
    instance_id = random_shuffle.targets.result[count.index]
  }

  provisioner "local-exec" {
    command = "aws ec2 terminate-instances --instance-ids ${self.triggers.instance_id}"
  }
}
