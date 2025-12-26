module "tag_audit_test" {
  source = "../src" # Refers to the module in the parent 'src' directory

  resources_to_audit = [
    {
      arn  = "arn:aws:s3:::my-bucket-1"
      tags = { "Environment" = "prod", "Owner" = "ApocalypsAI" }
    },
    {
      arn  = "arn:aws:ec2:us-east-1:123456789012:instance/i-0abcdef1234567890"
      tags = { "Environment" = "dev" }
    },
    {
      arn  = "arn:aws:s3:::my-bucket-2"
      tags = {}
    },
    {
      arn  = "arn:aws:lambda:us-west-2:123456789012:function:my-function"
      tags = { "Environment" = "prod", "Owner" = "ApocalypsAI", "Project" = "Alpha" }
    }
  ]

  required_tags = {
    "Environment" = "" # Key must exist, value can be anything
    "Owner"       = "ApocalypsAI" # Key must exist and value must match
    "Project"     = "" # Key must exist, value can be anything
  }
}

output "tag_audit_test" {
  value = module.tag_audit_test.audit_report
}
