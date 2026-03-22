output "public_ip" {
  description = "Public IP address of the ephemeral playground instance."
  value       = aws_instance.playground_instance.public_ip
}

output "instance_id" {
  description = "ID of the ephemeral playground instance."
  value       = aws_instance.playground_instance.id
}

output "destroy_after_tag" {
  description = "Timestamp when the instance is tagged for destruction."
  value       = aws_instance.playground_instance.tags.DestroyAfter
}
