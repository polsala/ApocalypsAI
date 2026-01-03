# Production Chaos Monkey Example

This example demonstrates a production-ready setup of the Terraform Chaos Monkey module with comprehensive safety measures.

## Production Features

- **Conservative chaos intervals**: 24 hours
- **Single resource targeting**: Minimizes impact
- **Comprehensive exclusions**: Protects critical infrastructure
- **Weekly scheduling**: Chaos on Mondays at 2 AM
- **Full monitoring**: CloudWatch metrics and SNS notifications
- **Extended log retention**: 365 days for audit trails

## Safety Measures

1. **Resource exclusions**: All critical production resources excluded
2. **Environment filtering**: Only targets production-tagged resources
3. **Dry run mode**: Prevents accidental destruction during setup
4. **Rate limiting**: Conservative chaos frequency
5. **Monitoring**: Real-time alerts and metrics

## Production Deployment

1. **Review and customize exclusions**
   ```bash
   # Edit the excluded_resources list in main.tf
   # Add your critical production resources
   ```

2. **Configure notifications**
   ```bash
   # Set up SNS topic for chaos notifications
   # Configure CloudWatch alarms
   ```

3. **Test in dry run mode**
   ```bash
   terraform apply -var="dry_run=true"
   ```

4. **Enable actual chaos**
   ```bash
   terraform apply -var="dry_run=false"
   ```

## Monitoring

- **CloudWatch Logs**: `/aws/chaos-monkey/production`
- **CloudWatch Metrics**: Custom metrics for chaos events
- **SNS Notifications**: Alerts for all chaos events
- **CloudWatch Alarms**: Automatic alerting when chaos occurs

## Best Practices

1. **Start with dry run mode**
2. **Monitor logs closely for the first few runs**
3. **Gradually increase chaos frequency as confidence grows**
4. **Review and update exclusions regularly**
5. **Document chaos events and system responses**

## Cleanup

```bash
terraform destroy
```

**Warning**: This will remove all chaos monkey resources but will NOT restore any resources that were terminated by chaos events.
