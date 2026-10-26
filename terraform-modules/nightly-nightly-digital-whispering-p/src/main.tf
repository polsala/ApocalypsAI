resource "aws_s3_bucket" "whispering_post_bucket" {
  bucket = var.bucket_name
  acl    = "public-read" # For static website hosting

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  tags = {
    Project = var.project_name
    ManagedBy = "ApocalypsAI"
  }
}

resource "aws_s3_bucket_policy" "whispering_post_bucket_policy" {
  bucket = aws_s3_bucket.whispering_post_bucket.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "PublicReadGetObject",
        Effect    = "Allow",
        Principal = "*",
        Action    = "s3:GetObject",
        Resource  = "${aws_s3_bucket.whispering_post_bucket.arn}/*"
      }
    ]
  })
}

resource "aws_s3_bucket_object" "index_html" {
  bucket       = aws_s3_bucket.whispering_post_bucket.id
  key          = "index.html"
  content_type = "text/html"
  source       = "${path.module}/web/index.html"
  etag         = filemd5("${path.module}/web/index.html")
}

resource "aws_dynamodb_table" "whispers_table" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  ttl {
    attribute_name = "expirationTime"
    enabled        = true
  }

  tags = {
    Project = var.project_name
    ManagedBy = "ApocalypsAI"
  }
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.project_name}-lambda-exec-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
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

  tags = {
    Project = var.project_name
    ManagedBy = "ApocalypsAI"
  }
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution_policy" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy" "dynamodb_access_policy" {
  name        = "${var.project_name}-dynamodb-access-policy"
  description = "Allows Lambda to read/write to DynamoDB for the whispering post."
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Scan"
        ],
        Resource = aws_dynamodb_table.whispers_table.arn
      }
    ]
  })

  tags = {
    Project = var.project_name
    ManagedBy = "ApocalypsAI"
  }
}

resource "aws_iam_role_policy_attachment" "lambda_custom_dynamodb_policy_attachment" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.dynamodb_access_policy.arn
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda/whisper_processor.py"
  output_path = "/tmp/${var.project_name}-whisper-processor.zip"
}

resource "aws_lambda_function" "whisper_processor" {
  function_name    = "${var.project_name}-whisper-processor"
  handler          = "whisper_processor.lambda_handler"
  runtime          = "python3.9"
  role             = aws_iam_role.lambda_exec_role.arn
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = 30

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.whispers_table.name
      WHISPER_TTL_SECONDS = var.whisper_ttl_hours * 3600 # Pass TTL to Lambda
    }
  }

  tags = {
    Project = var.project_name
    ManagedBy = "ApocalypsAI"
  }
}

resource "aws_api_gateway_rest_api" "whisper_api" {
  name        = "${var.project_name}-whisper-api"
  description = "API for submitting and retrieving whispers for the Digital Whispering Post."

  tags = {
    Project = var.project_name
    ManagedBy = "ApocalypsAI"
  }
}

resource "aws_api_gateway_resource" "whispers_resource" {
  rest_api_id = aws_api_gateway_rest_api.whisper_api.id
  parent_id   = aws_api_gateway_rest_api.whisper_api.root_resource_id
  path_part   = "whispers"
}

resource "aws_api_gateway_method" "post_whisper_method" {
  rest_api_id   = aws_api_gateway_rest_api.whisper_api.id
  resource_id   = aws_api_gateway_resource.whispers_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "post_whisper_integration" {
  rest_api_id             = aws_api_gateway_rest_api.whisper_api.id
  resource_id             = aws_api_gateway_resource.whispers_resource.id
  http_method             = aws_api_gateway_method.post_whisper_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.whisper_processor.invoke_arn
}

resource "aws_api_gateway_method" "get_whispers_method" {
  rest_api_id   = aws_api_gateway_rest_api.whisper_api.id
  resource_id   = aws_api_gateway_resource.whispers_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_whispers_integration" {
  rest_api_id             = aws_api_gateway_rest_api.whisper_api.id
  resource_id             = aws_api_gateway_resource.whispers_resource.id
  http_method             = aws_api_gateway_method.get_whispers_method.http_method
  integration_http_method = "POST" # Lambda proxy integration always uses POST
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.whisper_processor.invoke_arn
}

resource "aws_lambda_permission" "apigateway_lambda_permission_post" {
  statement_id  = "AllowAPIGatewayInvokePost"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.whisper_processor.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.whisper_api.execution_arn}/*/POST/whispers"
}

resource "aws_lambda_permission" "apigateway_lambda_permission_get" {
  statement_id  = "AllowAPIGatewayInvokeGet"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.whisper_processor.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.whisper_api.execution_arn}/*/GET/whispers"
}

resource "aws_api_gateway_deployment" "whisper_api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.whisper_api.id
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.whispers_resource.id,
      aws_api_gateway_method.post_whisper_method.id,
      aws_api_gateway_integration.post_whisper_integration.id,
      aws_api_gateway_method.get_whispers_method.id,
      aws_api_gateway_integration.get_whispers_integration.id,
    ]))
  }
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "whisper_api_stage" {
  deployment_id = aws_api_gateway_deployment.whisper_api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.whisper_api.id
  stage_name    = "v1"

  tags = {
    Project = var.project_name
    ManagedBy = "ApocalypsAI"
  }
}
