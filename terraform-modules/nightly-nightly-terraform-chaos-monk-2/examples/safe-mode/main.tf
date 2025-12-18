module "chaos_monkey" {
  source = "../../"
  
  enabled = true
  intensity = 0.5
  safe_mode = true  # Only logs, doesn't destroy
  cloud_provider = "aws"
  region = "us-east-1"
  resources = [
    "aws_instance.test-1",
    "aws_instance.test-2"
  ]
}

resource "aws_instance" "test-1" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
}

resource "aws_instance" "test-2" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
}
