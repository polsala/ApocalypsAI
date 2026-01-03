import json
import os
import random
import logging
import boto3
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients
ec2_client = boto3.client('ec2')
rds_client = boto3.client('rds')
elasticache_client = boto3.client('elasticache')
sns_client = boto3.client('sns') if os.environ.get('SNS_TOPIC_ARN') else None


def get_resource_types():
    """Get configured resource types from environment variables."""
    resource_types_str = os.environ.get('RESOURCE_TYPES', 'ec2')
    return [rt.strip() for rt in resource_types_str.split(',')]


def get_exclude_tags():
    """Get excluded tags from environment variables."""
    exclude_tags_str = os.environ.get('EXCLUDE_TAGS', '{}')
    return json.loads(exclude_tags_str)


def is_resource_excluded(tags, exclude_tags):
    """Check if resource should be excluded based on tags."""
    if not exclude_tags or not tags:
        return False
    
    for tag in tags:
        key = tag.get('Key')
        value = tag.get('Value')
        if key in exclude_tags and exclude_tags[key] == value:
            return True
    return False


def get_ec2_instances():
    """Get all EC2 instances that are not excluded."""
    exclude_tags = get_exclude_tags()
    instances = []
    
    try:
        # Get all instances
        response = ec2_client.describe_instances()
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                # Skip terminated instances
                if instance['State']['Name'] in ['terminated', 'shutting-down']:
                    continue
                
                # Get instance tags
                tags = instance.get('Tags', [])
                
                # Check if excluded
                if is_resource_excluded(tags, exclude_tags):
                    logger.info(f"Skipping EC2 instance {instance['InstanceId']} due to exclusion tags")
                    continue
                
                instances.append({
                    'id': instance['InstanceId'],
                    'type': 'ec2',
                    'state': instance['State']['Name'],
                    'tags': tags
                })
                
    except Exception as e:
        logger.error(f"Error getting EC2 instances: {e}")
    
    return instances


def get_rds_instances():
    """Get all RDS instances that are not excluded."""
    exclude_tags = get_exclude_tags()
    instances = []
    
    try:
        response = rds_client.describe_db_instances()
        
        for db_instance in response['DBInstances']:
            # Skip instances that are being deleted
            if db_instance['DBInstanceStatus'] in ['deleting']:
                continue
            
            # Get DB instance tags
            tags_response = rds_client.list_tags_for_resource(
                ResourceName=db_instance['DBInstanceArn']
            )
            tags = tags_response.get('TagList', [])
            
            # Check if excluded
            if is_resource_excluded(tags, exclude_tags):
                logger.info(f"Skipping RDS instance {db_instance['DBInstanceIdentifier']} due to exclusion tags")
                continue
            
            instances.append({
                'id': db_instance['DBInstanceIdentifier'],
                'type': 'rds',
                'state': db_instance['DBInstanceStatus'],
                'arn': db_instance['DBInstanceArn'],
                'tags': tags
            })
            
    except Exception as e:
        logger.error(f"Error getting RDS instances: {e}")
    
    return instances


def get_elasticache_clusters():
    """Get all ElastiCache clusters that are not excluded."""
    exclude_tags = get_exclude_tags()
    clusters = []
    
    try:
        response = elasticache_client.describe_cache_clusters()
        
        for cluster in response['CacheClusters']:
            # Skip clusters that are being deleted
            if cluster['CacheClusterStatus'] in ['deleting']:
                continue
            
            # Get cluster tags
            tags_response = elasticache_client.list_tags_for_resource(
                ResourceName=cluster['ARN']
            )
            tags = tags_response.get('TagList', [])
            
            # Check if excluded
            if is_resource_excluded(tags, exclude_tags):
                logger.info(f"Skipping ElastiCache cluster {cluster['CacheClusterId']} due to exclusion tags")
                continue
            
            clusters.append({
                'id': cluster['CacheClusterId'],
                'type': 'elasticache',
                'state': cluster['CacheClusterStatus'],
                'arn': cluster['ARN'],
                'tags': tags
            })
            
    except Exception as e:
        logger.error(f"Error getting ElastiCache clusters: {e}")
    
    return clusters


def select_chaos_targets(all_resources, max_chaos):
    """Randomly select resources for chaos."""
    if not all_resources:
        return []
    
    # Randomize the list
    random.shuffle(all_resources)
    
    # Select up to max_chaos targets
    return all_resources[:max_chaos]


def terminate_ec2_instance(instance_id, dry_run=False):
    """Terminate an EC2 instance."""
    try:
        if dry_run:
            logger.info(f"[DRY RUN] Would terminate EC2 instance: {instance_id}")
            return True
        
        ec2_client.terminate_instances(InstanceIds=[instance_id])
        logger.info(f"Terminated EC2 instance: {instance_id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to terminate EC2 instance {instance_id}: {e}")
        return False


def delete_rds_instance(db_instance_identifier, dry_run=False):
    """Delete an RDS instance."""
    try:
        if dry_run:
            logger.info(f"[DRY RUN] Would delete RDS instance: {db_instance_identifier}")
            return True
        
        rds_client.delete_db_instance(
            DBInstanceIdentifier=db_instance_identifier,
            SkipFinalSnapshot=True,
            DeleteAutomatedBackups=True
        )
        logger.info(f"Deleted RDS instance: {db_instance_identifier}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to delete RDS instance {db_instance_identifier}: {e}")
        return False


def delete_elasticache_cluster(cache_cluster_id, dry_run=False):
    """Delete an ElastiCache cluster."""
    try:
        if dry_run:
            logger.info(f"[DRY RUN] Would delete ElastiCache cluster: {cache_cluster_id}")
            return True
        
        elasticache_client.delete_cache_cluster(
            CacheClusterId=cache_cluster_id
        )
        logger.info(f"Deleted ElastiCache cluster: {cache_cluster_id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to delete ElastiCache cluster {cache_cluster_id}: {e}")
        return False


def send_notification(message):
    """Send notification via SNS if configured."""
    if not sns_client or not os.environ.get('SNS_TOPIC_ARN'):
        return
    
    try:
        sns_client.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Subject='Chaos Monkey Report',
            Message=message
        )
        logger.info("Notification sent successfully")
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")


def lambda_handler(event, context):
    """Main Lambda handler for chaos monkey execution."""
    logger.info("Chaos Monkey execution started")
    
    # Check if enabled
    if not os.environ.get('ENABLED', 'true').lower() == 'true':
        logger.info("Chaos Monkey is disabled, skipping execution")
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Chaos Monkey is disabled'})
        }
    
    # Get configuration
    max_chaos = int(os.environ.get('MAX_CHAOS_PER_RUN', '3'))
    dry_run = os.environ.get('DRY_RUN', 'false').lower() == 'true'
    aws_region = os.environ.get('AWS_REGION', 'us-east-1')
    
    logger.info(f"Configuration: max_chaos={max_chaos}, dry_run={dry_run}, region={aws_region}")
    
    # Get all resources
    all_resources = []
    
    resource_types = get_resource_types()
    logger.info(f"Target resource types: {resource_types}")
    
    if 'ec2' in resource_types:
        all_resources.extend(get_ec2_instances())
    
    if 'rds' in resource_types:
        all_resources.extend(get_rds_instances())
    
    if 'elasticache' in resource_types:
        all_resources.extend(get_elasticache_clusters())
    
    logger.info(f"Found {len(all_resources)} eligible resources")
    
    # Select targets for chaos
    targets = select_chaos_targets(all_resources, max_chaos)
    logger.info(f"Selected {len(targets)} targets for chaos: {[t['id'] for t in targets]}")
    
    # Execute chaos
    chaos_results = []
    success_count = 0
    
    for target in targets:
        result = {
            'id': target['id'],
            'type': target['type'],
            'success': False,
            'error': None
        }
        
        try:
            if target['type'] == 'ec2':
                result['success'] = terminate_ec2_instance(target['id'], dry_run)
            elif target['type'] == 'rds':
                result['success'] = delete_rds_instance(target['id'], dry_run)
            elif target['type'] == 'elasticache':
                result['success'] = delete_elasticache_cluster(target['id'], dry_run)
            
            if result['success']:
                success_count += 1
                
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Error processing target {target['id']}: {e}")
        
        chaos_results.append(result)
    
    # Prepare summary
    timestamp = datetime.utcnow().isoformat()
    summary = {
        'timestamp': timestamp,
        'region': aws_region,
        'dry_run': dry_run,
        'total_resources_found': len(all_resources),
        'targets_selected': len(targets),
        'chaos_executed': success_count,
        'results': chaos_results
    }
    
    # Log summary
    logger.info(f"Chaos Monkey execution completed: {json.dumps(summary, indent=2)}")
    
    # Send notification
    message = f"""
Chaos Monkey Execution Report
============================

Timestamp: {timestamp}
Region: {aws_region}
Dry Run: {dry_run}

Summary:
- Total resources found: {len(all_resources)}
- Targets selected: {len(targets)}
- Chaos executed successfully: {success_count}

Results:
{chr(10).join([f"- {r['type'].upper()}: {r['id']} - {'SUCCESS' if r['success'] else 'FAILED'}" for r in chaos_results])}
"""
    
    send_notification(message)
    
    return {
        'statusCode': 200,
        'body': json.dumps(summary, indent=2)
    }
