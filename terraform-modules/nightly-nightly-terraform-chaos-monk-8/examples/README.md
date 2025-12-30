# Examples

This directory contains example configurations for different environments and use cases.

## Available Examples

### `production.tf`

Production environment configuration with:

- Very low chaos probability (0.5% per hour)
- Strict resource exclusions
- Conservative time windows
- Safe mode enabled
- Comprehensive monitoring and alerting

### `staging.tf`

Staging environment configuration with:

- Medium chaos probability (2% per hour)
- Moderate resource exclusions
- Business hours only
- Safe mode enabled
- Basic monitoring

### `development.tf`

Development environment configuration with:

- Higher chaos probability (10% per hour)
- Minimal exclusions
- Extended time windows
- Safe mode can be disabled for real testing
- Development-focused monitoring

## Usage

1. Copy the appropriate example file for your environment
2. Customize the configuration for your specific needs
3. Add the module to your Terraform configuration
4. Run `terraform apply`

## Best Practices

### Production

- Always keep safe mode enabled initially
- Start with very low probability
- Use strict tag-based exclusions
- Monitor closely and adjust gradually
- Have rollback plans ready

### Staging

- Use moderate probability for realistic testing
- Enable safe mode for initial testing
- Gradually increase probability as confidence grows
- Test recovery procedures thoroughly

### Development

- Can disable safe mode for real chaos testing
- Use higher probability for frequent testing
- Test all recovery scenarios
- Experiment with different configurations

## Monitoring

All examples include CloudWatch dashboard configurations for monitoring:

- Chaos events triggered
- Resources terminated
- Resources skipped
- Error rates
- Recovery times

Set up appropriate alerts based on your environment's requirements.

## Safety Considerations

- Always test in development first
- Use tag-based exclusions to protect critical resources
- Start with safe mode enabled
- Monitor closely during initial deployments
- Have clear rollback procedures
- Consider business impact and timing

## Contributing Examples

If you have useful example configurations, consider contributing them:

1. Create a new example file
2. Add appropriate documentation
3. Test the configuration
4. Submit a pull request

Examples should follow the same structure and include:

- Clear comments explaining the configuration
- Appropriate safety measures
- Monitoring and alerting setup
- Environment-specific considerations
