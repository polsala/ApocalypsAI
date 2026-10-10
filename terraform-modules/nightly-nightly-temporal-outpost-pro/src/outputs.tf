output "public_ip" {
  description = "The public IP address of the temporal outpost."
  value       = aws_instance.outpost.public_ip
}

output "instance_id" {
  description = "The ID of the temporal outpost EC2 instance."
  value       = aws_instance.outpost.id
}

output "destroy_command" {
  description = "The command to initiate the temporal outpost's self-destruct sequence."
  value       = "To initiate the temporal outpost's self-destruct sequence, run: terraform destroy -auto-approve"
}

output "self_destruct_reminder" {
  description = "A reminder about the outpost's ephemeral nature."
  value       = "This temporal outpost is intended to exist for approximately ${var.self_destruct_after_minutes} minutes. Please remember to run 'terraform destroy' when your mission is complete."
}
