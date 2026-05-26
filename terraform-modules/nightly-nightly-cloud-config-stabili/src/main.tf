resource "aws_s3_bucket" "critical_archive_bucket" {
  bucket = var.bucket_name
  acl    = "private" # Ensure private access by default

  tags = {
    Environment = "ApocalypsAI"
    Purpose     = "CriticalDataArchive"
    ManagedBy   = "NightlyCloudConfigStabilizer"
  }
}

# The "Cloud Configuration Stabilizer" null_resource acts as a sensor.
# It triggers a local script if the 'drift_check_signal' changes,
# simulating an an external system reporting configuration drift.
resource "null_resource" "cloud_config_stabilizer" {
  triggers = {
    # This trigger variable simulates input from an external drift detection system.
    # In a real scenario, this could be a data source querying actual cloud state
    # or an output from a monitoring tool.
    drift_check_signal = var.simulate_drift_signal
  }

  provisioner "local-exec" {
    command = <<EOT
      echo "Nightly Cloud Configuration Stabilizer: Initiating scan for bucket '${aws_s3_bucket.critical_archive_bucket.bucket}'..."
      if [ "${self.triggers.drift_check_signal}" == "DRIFT_DETECTED" ]; then
        echo "WARNING: Configuration Rift Detected! The ApocalypsAI Critical Archive bucket '${aws_s3_bucket.critical_archive_bucket.bucket}' has drifted from its desired state."
        echo "Immediate stabilization protocols are recommended. Consult the IaC Chrono-Engineers."
        exit 1 # Indicate a problem/drift
      else
        echo "ApocalypsAI Critical Archive bucket '${aws_s3_bucket.critical_archive_bucket.bucket}' is stable. No configuration rifts detected."
      fi
    EOT
    # Mock rationale: The local-exec command simulates the output of an external
    # configuration drift detection system. The 'simulate_drift_signal' variable
    # allows for deterministic, offline testing of both stable and drifted states
    # without requiring actual cloud provider interaction or complex mock providers.
  }
}

output "archive_bucket_name" {
  value       = aws_s3_bucket.critical_archive_bucket.bucket
  description = "The name of the critical ApocalypsAI archive S3 bucket."
}

output "stabilizer_status" {
  value       = null_resource.cloud_config_stabilizer.triggers.drift_check_signal
  description = "The current status signal from the Cloud Configuration Stabilizer."
}
