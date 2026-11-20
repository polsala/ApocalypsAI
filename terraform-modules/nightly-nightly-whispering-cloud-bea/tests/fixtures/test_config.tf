module "test_beacon" {
  source = "../../src" # Path to the module under test

  bucket_name_prefix  = "test-apocalypsai-beacon"
  aws_region          = "us-east-1"
  beacon_message_html = "<h1>Test Signal</h1><p>This is a test message.</p>"
}
