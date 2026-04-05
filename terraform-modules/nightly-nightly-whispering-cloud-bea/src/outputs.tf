output "api_endpoint" {
  description = "The URL of the API Gateway endpoint for sending whispers."
  value       = aws_api_gateway_v2_stage.beacon_stage.invoke_url
}

output "lambda_function_name" {
  description = "The name of the deployed Lambda function."
  value       = aws_lambda_function.beacon_lambda.function_name
}
