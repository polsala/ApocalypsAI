# Minimal Chaos Monkey Example

This example demonstrates the most basic setup of the Terraform Chaos Monkey module.

## Quick Start

1. **Navigate to the example directory**
   ```bash
   cd examples/minimal
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

## Configuration

The minimal example includes:

- **Chaos enabled**: `true`
- **Interval**: 1 hour
- **Max resources per run**: 1
- **Target type**: EC2 instances only
- **Dry run**: `true` (safe mode)

## What It Does

- Creates a single test EC2 instance
- Configures chaos monkey to target EC2 instances
- Runs chaos every hour (dry run mode)
- Logs all chaos events to CloudWatch

## Safety

- Dry run mode prevents actual destruction
- Only one resource targeted per run
- Comprehensive logging for audit trails

## Next Steps

After testing the minimal example:

1. Try the [complete example](../complete/)
2. Configure for your specific resource types
3. Set up monitoring and alerting
4. Gradually increase chaos frequency

## Cleanup

```bash
terraform destroy
```
