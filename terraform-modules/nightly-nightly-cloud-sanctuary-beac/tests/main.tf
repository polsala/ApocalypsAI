terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

module "test_beacon" {
  source = "../src"

  project_name      = "test-project"
  environment       = "test"
  content_file_path = "${path.module}/test_content.html"
}
