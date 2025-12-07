output "beacon_url" {
  description = "The URL of the deployed API Gateway endpoint."
  value       = aws_apigatewayv2_api.morale_beacon_api.api_endpoint
}
