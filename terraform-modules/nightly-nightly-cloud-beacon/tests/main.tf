module "test_beacon" {
  source = "../src"

  bucket_name_prefix = "test-apocalypsai-beacon"
  index_document     = "test-index.html"
  error_document     = "test-error.html"
  tags = {
    Test        = "true"
    Environment = "Test"
  }
}

output "test_website_endpoint" {
  value = module.test_beacon.website_endpoint
}

output "test_cloudfront_domain_name" {
  value = module.test_beacon.cloudfront_domain_name
}
