module "test_sanctuary_beacon" {
  source = "../src"

  region              = "us-east-1"
  beacon_message      = "Test Beacon Message for Validation"
  create_dns_record   = false # Set to false for offline validation
  domain_name         = "test.example.com"
  subdomain           = "test-beacon"
}
