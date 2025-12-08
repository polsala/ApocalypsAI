output "api_gateway_url" {
  description = "The base URL of the Starlight Signal Reflector API Gateway endpoint."
  value       = aws_api_gateway_stage.starlight_stage.invoke_url
}
