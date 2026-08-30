variable "bucket_name" {
  description = "The name for the critical ApocalypsAI archive S3 bucket."
  type        = string
  default     = "apocalypsai-critical-archive-stable-12345" # Unique default
}

variable "simulate_drift_signal" {
  description = "A signal to simulate configuration drift detection. Set to 'DRIFT_DETECTED' to simulate a rift."
  type        = string
  default     = "STABLE"
}
