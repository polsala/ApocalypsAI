provider "aws" {
  region = "us-east-1"
  # Mock rationale: These tests use a mock AWS provider to run offline and deterministically.
  # No actual AWS credentials or network calls are made.
  # The mock simulates the provider's behavior for planning and asserting resource attributes.
  mock_behavior = "plan"
}

run "defaults" {
  variables = {
    bucket_name = "test-beacon-bucket"
  }

  assert {
    # Check if S3 bucket is planned for creation
    condition     = aws_s3_bucket.website_bucket.id != null
    error_message = "S3 bucket 'website_bucket' should be created."
  }

  assert {
    # Check if CloudFront distribution is planned for creation
    condition     = aws_cloudfront_distribution.website_cdn.id != null
    error_message = "CloudFront distribution 'website_cdn' should be created."
  }

  assert {
    # Check if OAC is planned for creation
    condition     = aws_cloudfront_origin_access_control.oac.id != null
    error_message = "CloudFront Origin Access Control 'oac' should be created."
  }

  assert {
    # Check if S3 bucket policy is planned for creation
    condition     = aws_s3_bucket_policy.website_bucket_policy.id != null
    error_message = "S3 bucket policy 'website_bucket_policy' should be created."
  }

  assert {
    # Check default_root_object is set correctly
    condition     = aws_cloudfront_distribution.website_cdn.default_root_object == "index.html"
    error_message = "CloudFront default_root_object should be 'index.html'."
  }

  assert {
    # Check that the S3 bucket policy contains the OAC ARN in its condition
    # For mock_behavior = "plan", we can only check attributes that are known at plan time.
    # The policy content itself is a string, so checking for substring is feasible.
    condition     = contains(aws_s3_bucket_policy.website_bucket_policy.policy, aws_cloudfront_origin_access_control.oac.arn)
    error_message = "S3 bucket policy should reference the OAC ARN."
  }

  assert {
    # Check that the CloudFront origin points to the S3 bucket's regional domain name
    condition     = aws_cloudfront_distribution.website_cdn.origin[0].domain_name == aws_s3_bucket.website_bucket.bucket_regional_domain_name
    error_message = "CloudFront origin domain_name should match S3 bucket regional domain name."
  }

  assert {
    # Check that the CloudFront origin uses the OAC ID
    condition     = aws_cloudfront_distribution.website_cdn.origin[0].origin_access_control_id == aws_cloudfront_origin_access_control.oac.id
    error_message = "CloudFront origin_access_control_id should match OAC ID."
  }
}

run "with_custom_domain" {
  variables = {
    bucket_name         = "test-custom-domain-beacon"
    aliases             = ["custom.example.com"]
    acm_certificate_arn = "arn:aws:acm:us-east-1:123456789012:certificate/mock-cert-id"
  }

  assert {
    condition     = contains(aws_cloudfront_distribution.website_cdn.aliases, "custom.example.com")
    error_message = "CloudFront distribution should have custom domain alias."
  }

  assert {
    condition     = aws_cloudfront_distribution.website_cdn.viewer_certificate[0].acm_certificate_arn == "arn:aws:acm:us-east-1:123456789012:certificate/mock-cert-id"
    error_message = "CloudFront distribution should use provided ACM certificate."
  }

  assert {
    condition     = aws_cloudfront_distribution.website_cdn.viewer_certificate[0].ssl_support_method == "sni-only"
    error_message = "CloudFront distribution SSL support method should be sni-only for custom cert."
  }
}

run "with_custom_error_document" {
  variables = {
    bucket_name    = "test-error-doc-beacon"
    error_document = "404.html"
  }

  assert {
    condition     = length(aws_cloudfront_distribution.website_cdn.custom_error_response) == 1
    error_message = "CloudFront distribution should have one custom error response."
  }

  assert {
    condition     = aws_cloudfront_distribution.website_cdn.custom_error_response[0].error_code == 404
    error_message = "Custom error response error_code should be 404."
  }

  assert {
    condition     = aws_cloudfront_distribution.website_cdn.custom_error_response[0].response_page_path == "/404.html"
    error_message = "Custom error response response_page_path should be /404.html."
  }
}
