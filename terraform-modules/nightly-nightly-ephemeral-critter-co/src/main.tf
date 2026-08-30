# main.tf - Defines the ephemeral cloud critter (AWS EC2 instance)

resource "aws_instance" "critter" {
  ami           = var.ami_id
  instance_type = var.instance_type
  tags = merge(
    {
      "Name"        = "${var.name_prefix}-critter",
      "Environment" = "Ephemeral",
      "ManagedBy"   = "ApocalypsAI"
    },
    var.additional_tags
  )

  # For simplicity, we're not configuring VPC, subnets, security groups here.
  # In a real-world scenario, these would be inputs or derived.
  # We'll assume default VPC/subnet for basic functionality.
  # Ensure your AWS credentials are configured.
}
