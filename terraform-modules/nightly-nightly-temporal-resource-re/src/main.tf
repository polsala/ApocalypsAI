# Data source to fetch details of the source EC2 instance
data "aws_instance" "source" {
  instance_id = var.source_instance_id
  # Mock rationale: This provider alias is expected to be configured in the root module
  # where this module is called. It points to the region of the source instance.
  # For testing, it's mocked in tests/main.tf.
  provider    = aws.source
}

# Data source to find default VPC in the target region
data "aws_vpc" "default_vpc" {
  # Mock rationale: This provider alias is expected to be configured in the root module
  # where this module is called. It points to the target region.
  # For testing, it's mocked in tests/main.tf.
  provider = aws.target
  default  = true
}

# Data source to find default subnet in the target region
data "aws_subnet_ids" "default_subnet" {
  # Mock rationale: This provider alias is expected to be configured in the root module
  # where this module is called. It points to the target region.
  # For testing, it's mocked in tests/main.tf.
  provider = aws.target
  vpc_id   = data.aws_vpc.default_vpc.id
  filter {
    name   = "default-for-az"
    values = ["true"]
  }
}

# Data source to find default security group in target region
data "aws_security_group" "default_sg" {
  # Mock rationale: This provider alias is expected to be configured in the root module
  # where this module is called. It points to the target region.
  # For testing, it's mocked in tests/main.tf.
  provider = aws.target
  vpc_id   = data.aws_vpc.default_vpc.id
  name     = "default"
}

resource "aws_instance" "echo" {
  # Mock rationale: This provider alias is expected to be configured in the root module
  # where this module is called. It points to the target region.
  # For testing, it's mocked in tests/main.tf.
  provider = aws.target

  ami           = coalesce(var.ami_override, data.aws_instance.source.ami)
  instance_type = coalesce(var.instance_type_override, data.aws_instance.source.instance_type)

  # Use provided subnet_id or attempt to find a default one
  subnet_id = var.subnet_id != null ? var.subnet_id : (
    length(data.aws_subnet_ids.default_subnet.ids) > 0 ? data.aws_subnet_ids.default_subnet.ids[0] : null
  )

  # Use provided security_group_ids or attempt to find the default security group
  vpc_security_group_ids = length(var.security_group_ids) > 0 ? var.security_group_ids : (
    data.aws_security_group.default_sg.id != null ? [data.aws_security_group.default_sg.id] : []
  )

  # Copy tags from source, then add/override with custom tags
  tags = merge(
    data.aws_instance.source.tags,
    {
      "Name"                       = "${var.replica_name_prefix}-${data.aws_instance.source.id}"
      "TemporalEchoSourceInstance" = data.aws_instance.source.id
      "TemporalEchoSourceRegion"   = data.aws_instance.source.availability_zone
      "TemporalEchoTargetRegion"   = var.target_region
    },
    var.tags_to_add
  )

  # Optional: Copy user data if present
  user_data = data.aws_instance.source.user_data_base64 != "" ? base64decode(data.aws_instance.source.user_data_base64) : null

  # Optional: Copy key name if present
  key_name = data.aws_instance.source.key_name

  # Optional: Copy volume details (simplified, only root block device for now)
  # Ensure root_block_device exists before accessing its elements
  dynamic "root_block_device" {
    for_each = length(data.aws_instance.source.root_block_device) > 0 ? [1] : []
    content {
      volume_size = data.aws_instance.source.root_block_device[0].volume_size
      volume_type = data.aws_instance.source.root_block_device[0].volume_type
      encrypted   = data.aws_instance.source.root_block_device[0].encrypted
    }
  }
}
