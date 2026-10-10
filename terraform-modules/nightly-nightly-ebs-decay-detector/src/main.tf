data "aws_ebs_volumes" "unattached" {
  filter {
    name   = "status"
    values = ["available"]
  }

  tags = var.tags_filter
}

output "unattached_ebs_volume_ids" {
  description = "A list of IDs of unattached EBS volumes."
  value       = data.aws_ebs_volumes.unattached.ids
}

output "unattached_ebs_volumes_count" {
  description = "The count of unattached EBS volumes found."
  value       = length(data.aws_ebs_volumes.unattached.ids)
}

output "unattached_ebs_volumes_details" {
  description = "Details of unattached EBS volumes."
  value = [
    for volume in data.aws_ebs_volumes.unattached.volumes : {
      id                = volume.id
      size              = volume.size
      type              = volume.type
      iops              = volume.iops
      encrypted         = volume.encrypted
      tags              = volume.tags
      create_time       = volume.create_time
      availability_zone = volume.availability_zone
    }
  ]
}
