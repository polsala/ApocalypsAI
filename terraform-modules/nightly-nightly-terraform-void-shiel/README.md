# Nightly Terraform Void Shield

A whimsical-yet-useful Terraform module that creates a mock cloud firewall with randomized security groups for testing and demos. Perfect for creating isolated test environments or demonstrating security concepts.

## Features
- Generates random security group rules
- Supports multiple cloud providers (AWS, GCP, Azure)
- Includes comprehensive test suite
- Fully self-contained

## Usage

```hcl
module "void_shield" {
  source = "./src"
  
  # Basic configuration
  environment = "test"
  region      = "us-east-1"
  
  # Security rules
  allow_ssh_from = ["10.0.0.0/16"]
  allow_http_from = ["0.0.0.0/0"]
  allow_https_from = ["0.0.0.0/0"]
}
```

## Testing

Run the test suite:

```bash
cd tests && terraform init && terraform plan
```

## License

MIT
