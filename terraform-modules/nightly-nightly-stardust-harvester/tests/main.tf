module "stardust_harvester_test" {
  source = "../" # Refers to the parent directory where main.tf, variables.tf, outputs.tf reside

  bucket_prefix = "test-stardust-collector"
  environment   = "test"

  enable_versioning = true
  transition_to_ia_days = 1
  expire_objects_days = 2
  abort_incomplete_multipart_upload_days = 1

  enable_notifications = true
  notification_filter_prefix = "important-stardust/"
}

module "stardust_harvester_no_notifications_test" {
  source = "../"

  bucket_prefix = "test-stardust-no-notify"
  environment   = "test"

  enable_versioning = false
  transition_to_ia_days = 5
  expire_objects_days = 10
  abort_incomplete_multipart_upload_days = 3

  enable_notifications = false
}
