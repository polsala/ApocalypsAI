provider "aws" {
  region = "us-east-1" # Mock rationale: Region is required for provider, but no actual AWS call is made during 'terraform plan'.
}

module "test_anomaly_beacon" {
  source = "../src"

  bucket_name_prefix   = "apocalypsai-test-beacon-"
  temporal_signature   = "TEST_SIG_ALPHA"
  beacon_frequency     = "DAILY"
  anomaly_classification = "MINOR_RIPPLE"
  archive_days         = 7
  expire_days          = 14
}
