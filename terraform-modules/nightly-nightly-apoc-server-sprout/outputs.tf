output "server_tags" {
  value = aws_instance.survival_server.*.tags
  description = "Survival server metadata tags"
}

output "server_count" {
  value = length(aws_instance.survival_server)
  description = "Number of servers in the sprout cluster"
}
