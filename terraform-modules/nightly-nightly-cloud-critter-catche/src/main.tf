resource "aws_instance" "critter" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = null # No key pair needed for self-terminating critter
  vpc_security_group_ids      = var.vpc_security_group_ids
  subnet_id                   = var.subnet_id
  associate_public_ip_address = true # Assign a public IP for easy access (if needed)

  # Whimsical user data script for self-termination
  user_data = <<-EOF
              #!/bin/bash
              echo "Hello from ${var.critter_name}! I am a cloud critter, born at $(date)."
              echo "My lifespan is ${var.lifespan_minutes} minutes. Enjoy me while I last!"
              # Schedule shutdown for termination
              sudo shutdown -h +${var.lifespan_minutes} "Critter self-destruct sequence initiated. Farewell!"
              EOF

  # Ensure the instance terminates when it shuts down
  instance_initiated_shutdown_behavior = "terminate"

  tags = {
    Name        = "Critter-${var.critter_name}"
    Environment = "Ephemeral"
    Purpose     = "NightlyCloudCritterCatcher"
    Lifespan    = "${var.lifespan_minutes}min"
  }

  # Prevent accidental destruction of the module itself, but allow the instance to terminate itself.
  # The instance_initiated_shutdown_behavior handles the actual termination.
  lifecycle {
    prevent_destroy = false
  }
}
