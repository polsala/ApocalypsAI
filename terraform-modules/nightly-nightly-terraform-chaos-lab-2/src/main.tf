terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "resource_tags" {
  description = "Tags to identify chaos-ready resources"
  type        = map(any)
}

variable "destruction_ratio" {
  description = "Ratio of resources to destroy (0.0 - 1.0)"
  type        = number
  default     = 0.5
}

variable "dry_run" {
  description = "Enable dry-run mode (no actual deletion)"
  type        = bool
  default     = true
}

locals {
  all_resources = flatten([
    [for instance in data.aws_instances.chaos : {
      type = "aws_instance"
      id   = instance.ids...
    }],
    [for lb in data.aws_lb.chaos : {
      type = "aws_lb"
      id   = lb.arn
    }]
  ])

  selected_count = floor(length(local.all_resources) * var.destruction_ratio)
  selected_resources = slice(shuffle(local.all_resources), 0, local.selected_count)
}

data "aws_instances" "chaos" {
  filter {
    name   = "tag:Environment"
    values = [lookup(var.resource_tags, "Environment", "test")]
  }

  filter {
    name   = "tag:ChaosReady"
    values = ["true"]
  }
}

data "aws_lb" "chaos" {
  tags = var.resource_tags
}

resource "null_resource" "destroy_resources" {
  count = var.dry_run ? 0 : length(local.selected_resources)

  triggers = {
    resource_id = local.selected_resources[count.index].id
  }

  provisioner "local-exec" {
    command = "echo 'Destroying ${local.selected_resources[count.index].type} ${local.selected_resources[count.index].id}'"
  }
}
