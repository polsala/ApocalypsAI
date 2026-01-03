# Chaos Monkey Module

This is the main Chaos Monkey module that can be included in other Terraform configurations.

## Usage

```hcl
module "chaos_monkey" {
  source = "git::https://github.com/polsala/ApocalypsAI.git//modules/chaos-monkey?ref=main"
  
  chaos_enabled = true
  dry_run       = true
}
```

## Inputs

See `variables.tf` for complete input documentation.

## Outputs

See `outputs.tf` for complete output documentation.

## Examples

- `examples/complete/` - Complete example with all features
- `examples/minimal/` - Minimal configuration
- `examples/production/` - Production-ready configuration

## Requirements

- Terraform >= 1.0
- AWS provider >= 4.0
- Appropriate IAM permissions for chaos operations

## Safety Guidelines

1. **Always start with dry run mode**
2. **Exclude critical resources**
3. **Use conservative chaos intervals**
4. **Monitor logs and metrics**
5. **Test in non-production environments first**

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.
