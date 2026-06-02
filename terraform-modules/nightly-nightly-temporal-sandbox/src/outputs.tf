output "sandbox_id" {
  description = "The ID of the deployed EC2 instance."
  value       = aws_instance.temporal_sandbox_instance.id
}

output "expiry_timestamp" {
  description = "The UTC timestamp (RFC3339) when the sandbox is intended to expire."
  value       = time_static.expiry_timestamp.rfc3339
}

output "vpc_id" {
  description = "The ID of the created VPC."
  value       = aws_vpc.temporal_sandbox_vpc.id
}

output "subnet_id" {
  description = "The ID of the created subnet."
  value       = aws_subnet.temporal_sandbox_subnet.id
}
