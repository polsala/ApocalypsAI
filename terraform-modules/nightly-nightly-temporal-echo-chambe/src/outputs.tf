output "instance_id" {
  description = "The ID of the created EC2 instance."
  value       = aws_instance.echo_chamber.id
}

output "public_ip" {
  description = "The public IP address of the EC2 instance."
  value       = aws_instance.echo_chamber.public_ip
}

output "termination_schedule_name" {
  description = "The name of the CloudWatch Event Rule for termination."
  value       = aws_cloudwatch_event_rule.termination_schedule.name
}
