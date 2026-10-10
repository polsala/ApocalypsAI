# Void Bridge Terraform Module

This module creates a dummy AWS security group named **void-bridge** with a set of randomized, harmless ingress rules. The rules only allow traffic on port **0** (a reserved, non‑routable port) and are purely whimsical – they do not expose any real services.

## Features
- Generates a security group with a custom name.
- Adds a configurable number of ingress rules, each pointing to a random CIDR block within `10.0.0.0/8`.
- All rules use port `0` and protocol `-1` (all protocols) – effectively a no‑op.
- Outputs the security group ID for downstream modules.

## Usage
```hcl
module "void_bridge" {
  source      = "git::https://github.com/yourorg/terraform-void-bridge.git"
  name        = "my-void-bridge"
  vpc_id      = "vpc-0abcd1234efgh5678"
  rule_count  = 3
}
```

## Variables
| Name | Description | Type | Default |
|------|-------------|------|---------|
| `name` | Name of the security group | `string` | n/a |
| `vpc_id` | VPC where the security group will be created | `string` | n/a |
| `rule_count` | Number of random ingress rules to create | `number` | `1` |

## Outputs
| Name | Description |
|------|-------------|
| `security_group_id` | The ID of the created security group |

## Disclaimer
This module is intended for fun and educational purposes only. The generated rules do not open any real ports and should not be used in production environments.
