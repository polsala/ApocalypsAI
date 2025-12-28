provider "aws" {
  region = "us-east-1"
  # Mock rationale: For offline testing, we don't need actual AWS credentials.
  # The 'terraform init -backend=false' and 'terraform validate' commands
  # will check syntax and variable resolution without attempting to authenticate.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
}

module "test_nomad_node" {
  source = "../src"

  name_prefix           = "test-nomad-node"
  region                = "us-east-1"
  ami_id                = "ami-0abcdef1234567890" # Placeholder AMI ID
  instance_type         = "t3.nano"
  key_name              = "test-key"
  vpc_security_group_ids = ["sg-0123456789abcdef0"]
  subnet_ids            = ["subnet-0fedcba9876543210", "subnet-0123456789abcdef"]
  min_size              = 1
  max_size              = 2
  desired_capacity      = 1
  user_data             = "#!/bin/bash\necho 'Hello from Nomad Node!' > /tmp/hello.txt"

  tags = {
    Environment = "Test"
    Owner       = "ApocalypsAI"
  }
}

output "test_asg_name" {
  value = module.test_nomad_node.asg_name
}
