resource "aws_security_group" "outpost_sg" {
  name        = "${var.outpost_name}-sg"
  description = "Allow SSH access to the Temporal Anomaly Outpost"
  vpc_id      = data.aws_vpc.default.id # Assumes a default VPC exists

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidrs
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.outpost_name}-sg"
  }
}

resource "aws_instance" "temporal_outpost" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_name
  vpc_security_group_ids = [aws_security_group.outpost_sg.id]

  user_data = <<-"EOF"
    #!/bin/bash
    echo "Starting Temporal Anomaly Detector setup..." >> /var/log/temporal_anomaly_detector.log
    yum update -y
    yum install -y cronie

    # Create the anomaly detection script
    cat << 'EOT' > /usr/local/bin/temporal_anomaly_detector.sh
    #!/bin/bash
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    ANOMALY_STATUS="Nominal"
    # In a real scenario, this would call an external API, check system metrics, etc.
    # For now, it's a whimsical placeholder.
    if (( RANDOM % 100 < 5 )); then # 5% chance of a "minor anomaly"
      ANOMALY_STATUS="Minor Temporal Fluctuation Detected!"
    elif (( RANDOM % 100 < 1 )); then # 1% chance of a "major anomaly"
      ANOMALY_STATUS="MAJOR TEMPORAL DISTORTION DETECTED! Seek shelter!"
    fi
    echo "${TIMESTAMP} - Outpost ${HOSTNAME} reports: ${ANOMALY_STATUS}" >> /var/log/temporal_anomaly_detector.log
    EOT

    chmod +x /usr/local/bin/temporal_anomaly_detector.sh

    # Add cron job to run every 5 minutes
    (crontab -l 2>/dev/null; echo "*/5 * * * * /usr/local/bin/temporal_anomaly_detector.sh") | crontab -

    echo "Temporal Anomaly Detector setup complete. Monitoring initiated." >> /var/log/temporal_anomaly_detector.log
  EOF

  tags = {
    Name = var.outpost_name
  }
}

# Data source to get the default VPC ID
data "aws_vpc" "default" {
  default = true
}
