# Example: Basic Chaos Monkey Configuration

provider "aws" {
  region = "us-east-1"
}

module "chaos_monkey" {
  source = "../.."
  
  # Basic configuration
  prefix           = "example-chaos"
  chaos_schedule   = "rate(1 hour)"  # Every hour
  resource_types   = ["ec2"]
  max_chaos_per_run = 1
  dry_run          = true  # Start with dry run
  
  # Exclude production resources
  exclude_tags = {
    Environment = "production"
    Critical    = "true"
  }
}

# Example EC2 instance that would be eligible for chaos
resource "aws_instance" "test_instance" {
  ami           = "ami-0c02fb55956c7d316"  # Amazon Linux 2 (us-east-1)
  instance_type = "t2.micro"
  
  tags = {
    Name        = "chaos-test-instance"
    Environment = "staging"  # Not production, so eligible for chaos
  }
}

# Example EC2 instance that would be protected
resource "aws_instance" "protected_instance" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"
  
  tags = {
    Name        = "protected-instance"
    Environment = "production"  # Protected from chaos
    Critical    = "true"        # Also protected
  }
}
