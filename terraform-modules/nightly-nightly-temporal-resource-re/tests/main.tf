# Mock rationale: For offline testing, we define mock AWS providers.
# These providers don't actually connect to AWS but allow Terraform to
# validate the configuration and generate a plan based on the mock setup.
# The 'aws_instance' data source is mocked by providing dummy values.
# The 'aws_vpc', 'aws_subnet_ids', and 'aws_security_group' data sources
# are also mocked to allow the module to resolve default network components.

# Mock source provider
provider "aws" {
  region = "us-east-1"
  # Mock rationale: In a real scenario, credentials would be configured.
  # For testing, we don't need actual credentials as we're not applying.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
  token      = "mock_token"
}

# Mock target provider
provider "aws" {
  alias  = "target"
  region = "us-west-1"
  # Mock rationale: Same as above, no real credentials needed for plan.
  access_key = "mock_access_key"
  secret_key = "mock_secret_key"
  token      = "mock_token"
}

# Mock data for the source instance
# Mock rationale: This data block simulates the output of a real 'aws_instance'
# data source without needing to query AWS.
data "aws_instance" "source" {
  instance_id = "i-mocksourceinstanceid"
  provider    = aws # Use the source provider alias

  # Mocked attributes
  ami               = "ami-mocksourceami"
  instance_type     = "t2.micro"
  availability_zone = "us-east-1a" # Added for TemporalEchoSourceRegion tag
  tags = {
    "OriginalTag1" = "Value1"
    "OriginalTag2" = "Value2"
  }
  user_data_base64 = base64encode("echo 'Hello from source!'")
  key_name         = "mock-key-pair"
  root_block_device {
    volume_size = 8
    volume_type = "gp2"
    encrypted   = false
  }
}

# Mock data for default VPC in target region
# Mock rationale: Simulates finding a default VPC in the target region.
data "aws_vpc" "default_vpc" {
  provider = aws.target
  default  = true
  # Mocked attributes
  id = "vpc-mockdefaultvpcid"
}

# Mock data for default subnet in target region
# Mock rationale: Simulates finding a default subnet in the target region.
data "aws_subnet_ids" "default_subnet" {
  provider = aws.target
  vpc_id   = data.aws_vpc.default_vpc.id
  filter {
    name   = "default-for-az"
    values = ["true"]
  }
  # Mocked attributes
  ids = ["subnet-mockdefaultsubnetid"]
}

# Mock data for default security group in target region
# Mock rationale: Simulates finding a default security group in the target region.
data "aws_security_group" "default_sg" {
  provider = aws.target
  vpc_id   = data.aws_vpc.default_vpc.id
  name     = "default"
  # Mocked attributes
  id = "sg-mockdefaultsgid"
}


module "test_echo_replication" {
  source = "../src" # Path to the module under test

  source_instance_id    = data.aws_instance.source.instance_id
  target_region         = "us-west-1"
  replica_name_prefix   = "test-echo"
  ami_override          = "ami-mockoverrideami"
  instance_type_override = "t3.small"
  tags_to_add = {
    "TestTag" = "TestValue"
  }
  subnet_id = data.aws_subnet_ids.default_subnet.ids[0]
  security_group_ids = [data.aws_security_group.default_sg.id]
}
