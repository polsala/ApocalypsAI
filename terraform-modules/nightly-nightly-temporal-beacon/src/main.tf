resource "aws_instance" "temporal_beacon" {
  ami           = var.ami_id
  instance_type = var.instance_type
  tags = {
    Name          = var.beacon_name
    ChronalAnchor = var.chronal_anchor_tag_value
    ManagedBy     = "ApocalypsAI-NightlyIntegrator"
  }
  # For simplicity, we're not attaching a VPC, subnet, or security group.
  # In a real-world scenario, these would be required.
  # This module focuses on the core instance and tagging.
}
