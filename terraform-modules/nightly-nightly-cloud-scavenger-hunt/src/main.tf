resource "aws_s3_bucket" "scavenger_bucket" {
  bucket = "${var.prefix}-scavenger-bucket-${random_id.bucket_suffix.hex}"
  acl    = "private"

  tags = {
    Environment    = "ApocalypsAI"
    Project        = "ScavengerHunt"
    ResourceType   = "PrepperStash"
    LootLevel      = "Rare"
    HiddenLocation = "SectorGamma"
    SurvivalKitID  = "Alpha-7"
  }
}

resource "aws_instance" "scavenger_ec2" {
  ami           = data.aws_ami.ubuntu.id # Using a common AMI for testing
  instance_type = var.instance_type
  key_name      = "apocalypsai-key" # Assumes a key pair exists or will be created
  
  tags = {
    Environment    = "ApocalypsAI"
    Project        = "ScavengerHunt"
    ResourceType   = "WastelandBeacon"
    LootLevel      = "Epic"
    HiddenLocation = "SectorDelta"
    SurvivalKitID  = "Beta-9"
  }
}

# Data source for a common Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["099720109477"] # Canonical
}

resource "aws_lambda_function" "scavenger_lambda" {
  filename         = "lambda_function_payload.zip"
  function_name    = "${var.prefix}-scavenger-lambda-${random_id.lambda_suffix.hex}"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "index.handler"
  runtime          = var.lambda_runtime
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  tags = {
    Environment    = "ApocalypsAI"
    Project        = "ScavengerHunt"
    ResourceType   = "AutomatedSentry"
    LootLevel      = "Legendary"
    HiddenLocation = "SectorEpsilon"
    SurvivalKitID  = "Gamma-12"
  }
}

resource "aws_iam_role" "lambda_exec" {
  name = "${var.prefix}-lambda-exec-role-${random_id.lambda_role_suffix.hex}"

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
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Create a dummy zip file for the Lambda function
data "archive_file" "lambda_zip" {
  type        = "zip"
  output_path = "lambda_function_payload.zip"
  source_content {
    content  = "exports.handler = async (event) => { console.log('Scavenger Lambda activated!'); return { statusCode: 200, body: 'Hello from Scavenger Lambda!' }; };"
    filename = "index.js"
  }
}

resource "aws_dynamodb_table" "scavenger_dynamodb" {
  name         = "${var.prefix}-scavenger-dynamodb-${random_id.dynamodb_suffix.hex}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Environment    = "ApocalypsAI"
    Project        = "ScavengerHunt"
    ResourceType   = "DataCache"
    LootLevel      = "Uncommon"
    HiddenLocation = "SectorZeta"
    SurvivalKitID  = "Delta-15"
  }
}

# Random ID for unique naming
resource "random_id" "bucket_suffix" {
  byte_length = 4
}
resource "random_id" "lambda_suffix" {
  byte_length = 4
}
resource "random_id" "lambda_role_suffix" {
  byte_length = 4
}
resource "random_id" "dynamodb_suffix" {
  byte_length = 4
}
