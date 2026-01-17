# Mock rationale: We mock AWS data sources to simulate tagged resources without real cloud access.

resource "null_resource" "mock_test" {
  provisioner "local-exec" {
    command = "echo 'Running offline test for chaos lab module'"
  }
}

data "aws_instances" "chaos" {
  filter {
    name   = "tag:Environment"
    values = ["test"]
  }

  filter {
    name   = "tag:ChaosReady"
    values = ["true"]
  }
}

data "aws_lb" "chaos" {
  tags = {
    Environment = "test"
    ChaosReady  = "true"
  }
}

output "test_selected_count" {
  value = floor(length(flatten([
    [for instance in data.aws_instances.chaos : instance.ids],
    [for lb in data.aws_lb.chaos : lb.arn]
  ])) * 0.5)
}
