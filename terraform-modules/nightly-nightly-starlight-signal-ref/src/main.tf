resource "aws_s3_bucket" "lambda_code_bucket" {
  bucket = "${var.project_name}-starlight-reflector-code-${random_string.bucket_suffix.result}"
  acl    = "private"

  tags = {
    Project = var.project_name
    Utility = "StarlightSignalReflector"
  }
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
  numeric = true
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda"
  output_path = "/tmp/${var.project_name}-starlight-reflector-lambda.zip"
}

resource "aws_s3_bucket_object" "lambda_code_upload" {
  bucket = aws_s3_bucket.lambda_code_bucket.id
  key    = "starlight_reflector.zip"
  source = data.archive_file.lambda_zip.output_path
  etag   = filemd5(data.archive_file.lambda_zip.output_path)
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.project_name}-starlight-reflector-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    Project = var.project_name
    Utility = "StarlightSignalReflector"
  }
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "starlight_reflector" {
  function_name    = "${var.project_name}-starlight-reflector"
  s3_bucket        = aws_s3_bucket.lambda_code_bucket.id
  s3_key           = aws_s3_bucket_object.lambda_code_upload.key
  handler          = "starlight_reflector.lambda_handler"
  runtime          = "python3.9"
  role             = aws_iam_role.lambda_exec_role.arn
  timeout          = 30
  memory_size      = 128

  environment {
    variables = {
      REFLECTOR_ID = "StarlightEcho-${random_id.reflector_id.hex}"
    }
  }

  tags = {
    Project = var.project_name
    Utility = "StarlightSignalReflector"
  }
}

resource "random_id" "reflector_id" {
  byte_length = 8
}

resource "aws_api_gateway_rest_api" "starlight_api" {
  name        = "${var.project_name}-StarlightSignalAPI"
  description = "API Gateway for Starlight Signal Reflector"

  tags = {
    Project = var.project_name
    Utility = "StarlightSignalReflector"
  }
}

resource "aws_api_gateway_resource" "proxy_resource" {
  rest_api_id = aws_api_gateway_rest_api.starlight_api.id
  parent_id   = aws_api_gateway_rest_api.starlight_api.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy_method" {
  rest_api_id   = aws_api_gateway_rest_api.starlight_api.id
  resource_id   = aws_api_gateway_resource.proxy_resource.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.starlight_api.id
  resource_id             = aws_api_gateway_resource.proxy_resource.id
  http_method             = aws_api_gateway_method.proxy_method.http_method
  integration_http_method = "POST" # Lambda proxy integration uses POST
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.starlight_reflector.invoke_arn
}

resource "aws_api_gateway_method" "root_method" {
  rest_api_id   = aws_api_gateway_rest_api.starlight_api.id
  resource_id   = aws_api_gateway_rest_api.starlight_api.root_resource_id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "root_lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.starlight_api.id
  resource_id             = aws_api_gateway_rest_api.starlight_api.root_resource_id
  http_method             = aws_api_gateway_method.root_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.starlight_reflector.invoke_arn
}

resource "aws_api_gateway_deployment" "starlight_deployment" {
  rest_api_id = aws_api_gateway_rest_api.starlight_api.id
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.proxy_resource.id,
      aws_api_gateway_method.proxy_method.id,
      aws_api_gateway_integration.lambda_integration.id,
      aws_api_gateway_method.root_method.id,
      aws_api_gateway_integration.root_lambda_integration.id,
    ]))
  }
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "starlight_stage" {
  deployment_id = aws_api_gateway_deployment.starlight_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.starlight_api.id
  stage_name    = "prod"

  tags = {
    Project = var.project_name
    Utility = "StarlightSignalReflector"
  }
}

resource "aws_lambda_permission" "apigw_lambda_permission" {
  statement_id  = "AllowAPIGatewayInvokeLambda"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.starlight_reflector.function_name
  principal     = "apigateway.amazonaws.com"

  # The /*/* part allows invocation from any stage, any method, any path
  source_arn = "${aws_api_gateway_rest_api.starlight_api.execution_arn}/*/*"
}

data "aws_partition" "current" {}
