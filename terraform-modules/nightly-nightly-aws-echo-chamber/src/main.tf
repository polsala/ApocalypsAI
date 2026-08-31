resource "aws_s3_bucket" "echo_chamber_bucket" {
  bucket = "${var.bucket_name_prefix}-${var.project_name}-echoes"
  tags = {
    Project = var.project_name
    Utility = "NightlyAWSEchoChamber"
  }
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.project_name}-echo-chamber-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_s3_access_policy" {
  name = "${var.project_name}-echo-chamber-s3-access"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ],
        Effect = "Allow",
        Resource = [
          aws_s3_bucket.echo_chamber_bucket.arn,
          "${aws_s3_bucket.echo_chamber_bucket.arn}/*"
        ]
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect = "Allow",
        Resource = "arn:aws:logs:${var.region}:*:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_s3_attach" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_s3_access_policy.arn
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda/echo_handler.py"
  output_path = "${path.module}/lambda/echo_handler.zip"
}

resource "aws_lambda_function" "echo_chamber_lambda" {
  function_name    = "${var.project_name}-echo-chamber-handler"
  handler          = "echo_handler.handler"
  runtime          = "python3.9"
  role             = aws_iam_role.lambda_exec_role.arn
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = 30

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.echo_chamber_bucket.bucket
    }
  }
}

resource "aws_api_gateway_rest_api" "echo_chamber_api" {
  name        = "${var.project_name}-EchoChamberAPI"
  description = "API for the Temporal Echo Chamber"
}

resource "aws_api_gateway_resource" "echo_resource" {
  rest_api_id = aws_api_gateway_rest_api.echo_chamber_api.id
  parent_id   = aws_api_gateway_rest_api.echo_chamber_api.root_resource_id
  path_part   = "echo"
}

resource "aws_api_gateway_method" "post_echo_method" {
  rest_api_id   = aws_api_gateway_rest_api.echo_chamber_api.id
  resource_id   = aws_api_gateway_resource.echo_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "post_echo_integration" {
  rest_api_id             = aws_api_gateway_rest_api.echo_chamber_api.id
  resource_id             = aws_api_gateway_resource.echo_resource.id
  http_method             = aws_api_gateway_method.post_echo_method.http_method
  integration_http_method = "POST" # Lambda invoke method
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.echo_chamber_lambda.invoke_arn
}

resource "aws_api_gateway_method" "get_echo_method" {
  rest_api_id   = aws_api_gateway_rest_api.echo_chamber_api.id
  resource_id   = aws_api_gateway_resource.echo_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_echo_integration" {
  rest_api_id             = aws_api_gateway_rest_api.echo_chamber_api.id
  resource_id             = aws_api_gateway_resource.echo_resource.id
  http_method             = aws_api_gateway_method.get_echo_method.http_method
  integration_http_method = "POST" # Lambda invoke method
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.echo_chamber_lambda.invoke_arn
}

resource "aws_lambda_permission" "apigw_lambda_permission_post" {
  statement_id  = "AllowAPIGatewayInvokePost"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.echo_chamber_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.echo_chamber_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "apigw_lambda_permission_get" {
  statement_id  = "AllowAPIGatewayInvokeGet"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.echo_chamber_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.echo_chamber_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "echo_chamber_deployment" {
  rest_api_id = aws_api_gateway_rest_api.echo_chamber_api.id
  triggers = {
    # NOTE: The "triggers" below are to force a new deployment when the Lambda or API Gateway methods change.
    # This is a common pattern to ensure changes are propagated.
    redeployment = sha1(jsonencode([
      aws_api_gateway_method.post_echo_method.id,
      aws_api_gateway_integration.post_echo_integration.id,
      aws_api_gateway_method.get_echo_method.id,
      aws_api_gateway_integration.get_echo_integration.id,
      aws_lambda_function.echo_chamber_lambda.last_modified,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "echo_chamber_stage" {
  deployment_id = aws_api_gateway_deployment.echo_chamber_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.echo_chamber_api.id
  stage_name    = "v1"
}
