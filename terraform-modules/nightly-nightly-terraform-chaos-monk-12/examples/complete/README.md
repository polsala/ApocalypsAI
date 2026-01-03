# Complete Chaos Monkey Example

This example demonstrates a complete setup of the Terraform Chaos Monkey module with:

- Multiple resource types (EC2, RDS, ElastiCache)
- Safety exclusions
- Dry run mode
- Comprehensive logging
- Metrics and monitoring

## Quick Start

1. **Clone and navigate to the example directory**
   ```bash
   cd examples/complete
   ```

2. **Initialize Terraform**
   ```bash
   terraform init
   ```

3. **Review the plan**
   ```bash
   terraform plan
   ```

4. **Apply the configuration**
   ```bash
   terraform apply
   ```

5. **Monitor chaos events**
   - Check CloudWatch logs: `/aws/chaos-monkey/staging`
   - Monitor CloudWatch metrics for chaos events
   - Review Terraform state for changes

## Configuration

The example is pre-configured with:

- **Chaos enabled**: `true`
- **Interval**: 2 hours
- **Max resources per run**: 3
- **Target types**: EC2, RDS, ElastiCache
- **Exclusions**: Production-critical resources
- **Dry run**: `true` (safe mode)

## Safety Features

- All critical resources are excluded
- Dry run mode prevents actual destruction
- Comprehensive logging for audit trails
- Resource filtering by environment tags

## Production Usage

To use in production:

1. Set `dry_run = false`
2. Configure appropriate exclusions
3. Set up SNS notifications
4. Monitor logs and metrics closely
5. Start with minimal chaos intervals

## Monitoring

- **CloudWatch Logs**: `/aws/chaos-monkey/{workspace}`
- **CloudWatch Metrics**: Custom metrics for chaos events
- **SNS Notifications**: Optional alerting for chaos events

## Cleanup

```bash
terraform destroy
```
