testcase "validate_outputs" {
  module.dir = "./"
  planfile = "plan.json"

  check {
    name = "vpc exists"
    condition = length(module.nomad_vpc.id) > 0
  }

  check {
    name = "minimum 2 subnets"
    condition = length(module.private_subnets.id) >= 2
  }

  check {
    name = "web URL format"
    condition = strcontains(module.web_url, "https://")
  }
}

mock {
  provider "aws" {
    region = "us-west-2"
  }
}
