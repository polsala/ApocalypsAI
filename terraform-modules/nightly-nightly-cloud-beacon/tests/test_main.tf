# Mock rationale: This test configuration uses a mock AWS provider to simulate resource creation
# without making actual API calls to AWS. This ensures deterministic and offline testing.
# The mock provider is configured to return predefined values for resource attributes,
# allowing assertions on the expected state of the Terraform module.

# Define the mock AWS provider for testing purposes.
# This block intercepts calls to the 'aws' provider and returns predefined values.
mock_provider "aws" {
  # Mock aws_s3_bucket resource
  mock_resource "aws_s3_bucket" "beacon_bucket" {
    bucket                      = var.bucket_name
    acl                         = "public-read"
    website = [{
      index_document = "index.html"
      error_document = "error.html"
    }]
    bucket_regional_domain_name = "${var.bucket_name}.s3.amazonaws.com"
    arn                         = "arn:aws:s3:::${var.bucket_name}"
    id                          = var.bucket_name
  }

  # Mock aws_s3_bucket_policy resource
  mock_resource "aws_s3_bucket_policy" "beacon_bucket_policy" {
    bucket = aws_s3_bucket.beacon_bucket.id
    policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          Sid       = "PublicReadGetObject",
          Effect    = "Allow",
          Principal = "*",
          Action    = ["s3:GetObject"],
          Resource  = ["${aws_s3_bucket.beacon_bucket.arn}/*"]
        }
      ]
    })
  }

  # Mock aws_cloudfront_origin_access_control resource
  mock_resource "aws_cloudfront_origin_access_control" "beacon_oac" {
    id = "E1234567890ABCDEF"
  }

  # Mock aws_cloudfront_distribution resource
  mock_resource "aws_cloudfront_distribution" "beacon_distribution" {
    enabled             = true
    is_ipv6_enabled     = true
    comment             = "CloudFront distribution for the Nightly Cloud Beacon"
    default_root_object = "index.html"
    domain_name         = "d1234567890abcdef.cloudfront.net"
    hosted_zone_id      = "Z2FDTNDATAQYW2" # Mock rationale: Standard CloudFront hosted zone ID.
    # Other attributes can be mocked if needed for assertions
  }

  # Mock aws_route53_record resource
  mock_resource "aws_route53_record" "beacon_cname" {
    zone_id = var.zone_id
    name    = var.domain_name
    type    = "A"
    alias = [{
      name                   = "d1234567890abcdef.cloudfront.net"
      zone_id                = "Z2FDTNDATAQYW2"
      evaluate_target_health = false
    }]
  }

  # Mock aws_s3_bucket_object resources
  mock_resource "aws_s3_bucket_object" "index_html" {
    bucket       = aws_s3_bucket.beacon_bucket.id
    key          = "index.html"
    content_type = "text/html"
    content      = "<html><body><h1>Hello from the Nightly Cloud Beacon!</h1><p>The ApocalypsAI community is here.</p></body></html>"
    acl          = "public-read"
  }

  mock_resource "aws_s3_bucket_object" "error_html" {
    bucket       = aws_s3_bucket.beacon_bucket.id
    key          = "error.html"
    content_type = "text/html"
    content      = "<html><body><h1>404 - Beacon Lost!</h1><p>The requested signal could not be found.</p></body></html>"
    acl          = "public-read"
  }
}

# Test case: Default beacon deployment
run "default_beacon_deployment" {
  variables {
    bucket_name = "apocalypsai-beacon-test-123"
  }

  command = plan

  assert {
    condition     = aws_s3_bucket.beacon_bucket.bucket == "apocalypsai-beacon-test-123"
    error_message = "S3 bucket name does not match expected value."
  }

  assert {
    condition     = aws_s3_bucket.beacon_bucket.website[0].index_document == "index.html"
    error_message = "S3 bucket index document not set correctly."
  }

  assert {
    condition     = aws_cloudfront_distribution.beacon_distribution.enabled == true
    error_message = "CloudFront distribution is not enabled."
  }

  assert {
    condition     = aws_cloudfront_distribution.beacon_distribution.default_root_object == "index.html"
    error_message = "CloudFront default root object not set correctly."
  }

  assert {
    condition     = aws_s3_bucket_object.index_html.key == "index.html"
    error_message = "Index HTML object not created."
  }

  assert {
    condition     = aws_s3_bucket_object.error_html.key == "error.html"
    error_message = "Error HTML object not created."
  }
}

# Test case: Beacon with custom domain
run "custom_domain_beacon_deployment" {
  variables {
    bucket_name = "apocalypsai-beacon-domain-test"
    domain_name = "beacon.example.com"
    zone_id     = "Z1EXAMPLEZONEID" # Mock rationale: A dummy zone ID for testing purposes.
  }

  command = plan

  assert {
    condition     = length(aws_route53_record.beacon_cname) == 1
    error_message = "Route 53 record not created when domain_name and zone_id are provided."
  }

  assert {
    condition     = aws_route53_record.beacon_cname[0].name == "beacon.example.com"
    error_message = "Route 53 record name does not match expected value."
  }
}

# Test case: Beacon without custom domain
run "no_custom_domain_beacon_deployment" {
  variables {
    bucket_name = "apocalypsai-beacon-no-domain"
    domain_name = ""
    zone_id     = ""
  }

  command = plan

  assert {
    condition     = length(aws_route53_record.beacon_cname) == 0
    error_message = "Route 53 record created when domain_name and zone_id are not provided."
  }
}
