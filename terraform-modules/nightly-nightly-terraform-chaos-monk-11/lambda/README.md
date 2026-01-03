# Chaos Monkey Lambda Function

This directory contains the Python Lambda function that implements the chaos engineering logic.

## Function Overview

The Lambda function:

1. **Discovers resources** - Scans for EC2 instances, RDS databases, and ElastiCache clusters
2. **Applies filters** - Excludes resources with specific tags
3. **Selects targets** - Randomly chooses resources for termination
4. **Executes chaos** - Terminates/deletes selected resources
5. **Reports results** - Logs actions and sends notifications

## Supported Resource Types

- **EC2 Instances** - Terminated using `terminate_instances`
- **RDS Instances** - Deleted using `delete_db_instance` (with skip final snapshot)
- **ElastiCache Clusters** - Deleted using `delete_cache_cluster`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RESOURCE_TYPES` | Comma-separated list of resource types to target | `ec2` |
| `EXCLUDE_TAGS` | JSON string of tags to exclude from chaos | `{}` |
| `MAX_CHAOS_PER_RUN` | Maximum resources to terminate per execution | `3` |
| `DRY_RUN` | Enable dry run mode (logs without executing) | `false` |
| `AWS_REGION` | AWS region for operations | `us-east-1` |
| `SNS_TOPIC_ARN` | SNS topic ARN for notifications | (optional) |

## Security Considerations

- The Lambda function requires minimal IAM permissions
- Resources can be protected using tag-based exclusion
- Dry run mode allows testing without actual resource termination
- All actions are logged to CloudWatch Logs

## Testing

The function can be tested locally by setting environment variables and running:

```bash
export RESOURCE_TYPES="ec2,rds"
export EXCLUDE_TAGS='{"Environment": "production"}'
export DRY_RUN="true"
python index.py
```

## Error Handling

The function includes comprehensive error handling:

- Resource discovery errors are logged but don't stop execution
- Individual resource termination failures don't affect other targets
- All errors are captured and included in the execution summary
- Notifications include both successes and failures
