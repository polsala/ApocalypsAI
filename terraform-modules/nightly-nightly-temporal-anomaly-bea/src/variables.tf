variable "bucket_name_prefix" {
  description = "A unique prefix for the S3 bucket name."
  type        = string
}

variable "temporal_signature" {
  description = "A whimsical signature for the temporal anomaly."
  type        = string
  default     = "UNKNOWN_SIGNATURE"
}

variable "beacon_frequency" {
  description = "The perceived frequency of temporal anomalies this beacon monitors."
  type        = string
  default     = "INFREQUENT"
}

variable "anomaly_classification" {
  description = "The classification of the temporal anomaly (e.g., 'Minor Ripple', 'Major Distortion')."
  type        = string
  default     = "UNCLASSIFIED"
}

variable "archive_days" {
  description = "Number of days after which objects are transitioned to GLACIER."
  type        = number
  default     = 30
}

variable "expire_days" {
  description = "Number of days after which objects are expired (deleted)."
  type        = number
  default     = 90
}
