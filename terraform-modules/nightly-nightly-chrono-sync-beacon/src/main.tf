resource "aws_security_group" "chrono_sync_beacon_sg" {
  name        = "chrono-sync-beacon-sg-${var.environment}"
  description = "Allow NTP traffic to Chrono-Sync Beacon"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 123
    to_port     = 123
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "NTP (UDP 123)"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "ChronoSyncBeacon-SG-${var.environment}"
    ManagedBy   = "ApocalypsAI"
    UtilityName = "nightly-chrono-sync-beacon"
  }
}

resource "aws_instance" "chrono_sync_beacon" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  vpc_security_group_ids = [aws_security_group.chrono_sync_beacon_sg.id]
  subnet_id              = var.subnet_id
  associate_public_ip_address = true

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y chrony
    systemctl enable chronyd
    systemctl start chronyd
    # Configure chrony to use public NTP servers and allow clients
    echo "server 0.pool.ntp.org iburst" >> /etc/chrony.conf
    echo "server 1.pool.ntp.org iburst" >> /etc/chrony.conf
    echo "server 2.pool.ntp.org iburst" >> /etc/chrony.conf
    echo "server 3.pool.ntp.org iburst" >> /etc/chrony.conf
    echo "allow 0.0.0.0/0" >> /etc/chrony.conf # Allow any client to query
    systemctl restart chronyd
    EOF

  tags = {
    Name        = "ChronoSyncBeacon-${var.environment}"
    ManagedBy   = "ApocalypsAI"
    UtilityName = "nightly-chrono-sync-beacon"
  }
}

check "instance_type_is_recommended" {
  precondition {
    condition     = contains(["t2.micro", "t3.small", "t3.medium"], var.instance_type)
    error_message = "Instance type '${var.instance_type}' is not a recommended type for a Chrono-Sync Beacon. Consider 't2.micro', 't3.small', or 't3.medium' for cost-effectiveness and stability."
  }
  # Mock rationale: This check is deterministic and offline, validating input variables against a predefined list.
}
