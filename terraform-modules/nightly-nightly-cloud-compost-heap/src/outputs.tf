output "compost_bucket_id" {
  description = "The ID of the S3 bucket for composted items."
  value       = var.enable_s3_compost_bucket ? aws_s3_bucket.compost_bucket[0].id : null
}

output "compost_bucket_arn" {
  description = "The ARN of the S3 bucket for composted items."
  value       = var.enable_s3_compost_bucket ? aws_s3_bucket.compost_bucket[0].arn : null
}

output "stale_ebs_config_rule_id" {
  description = "The ID of the AWS Config rule for stale EBS volumes."
  value       = var.enable_ebs_stale_volume_detector ? aws_config_rule.stale_ebs_volume_detector[0].id : null
}

output "stale_ebs_config_rule_arn" {
  description = "The ARN of the AWS Config rule for stale EBS volumes."
  value       = var.enable_ebs_stale_volume_detector ? aws_config_rule.stale_ebs_volume_detector[0].arn : null
}

output "stale_ec2_config_rule_id" {
  description = "The ID of the AWS Config rule for stale EC2 instances."
  value       = var.enable_ec2_stale_instance_detector ? aws_config_rule.stale_ec2_instance_detector[0].id : null
}

output "stale_ec2_config_rule_arn" {
  description = "The ARN of the AWS Config rule for stale EC2 instances."
  value       = var.enable_ec2_stale_instance_detector ? aws_config_rule.stale_ec2_instance_detector[0].arn : null
}

output "notification_topic_arn" {
  description = "The ARN of the SNS topic for notifications."
  value       = aws_sns_topic.notification_topic.arn
}
