output "chaos_garden_name" {
  description = "Name of the chaos garden"
  value       = local.chaos_name
}

output "chaos_vpc_id" {
  description = "ID of the chaos VPC"
  value       = aws_vpc.chaos_vpc.id
  sensitive   = false
}

output "chaos_subnet_ids" {
  description = "IDs of the chaos subnets"
  value       = aws_subnet.chaos_subnets[*].id
  sensitive   = false
}

output "chaos_security_group_id" {
  description = "ID of the chaos security group"
  value       = aws_security_group.chaos_sg.id
  sensitive   = false
}

output "chaos_instance_ids" {
  description = "IDs of the chaos EC2 instances"
  value       = var.enable_compute_chaos ? aws_instance.chaos_instances[*].id : []
  sensitive   = false
}

output "chaos_bucket_names" {
  description = "Names of the chaos S3 buckets"
  value       = var.enable_storage_chaos ? aws_s3_bucket.chaos_buckets[*].id : []
  sensitive   = false
}

output "chaos_rds_endpoint" {
  description = "Endpoint of the chaos RDS instance"
  value       = var.enable_compute_chaos && var.chaos_level == "high" ? aws_db_instance.chaos_rds[0].endpoint : ""
  sensitive   = false
}

output "chaos_lambda_arn" {
  description = "ARN of the chaos Lambda function"
  value       = var.enable_compute_chaos ? aws_lambda_function.chaos_lambda[0].arn : ""
  sensitive   = false
}

output "chaos_cloudwatch_dashboard_url" {
  description = "URL of the chaos CloudWatch dashboard"
  value       = var.enable_compute_chaos ? "https://console.aws.amazon.com/cloudwatch/home?region=${var.region}#dashboards:name=${aws_cloudwatch_dashboard.chaos_dashboard.dashboard_name}" : ""
  sensitive   = false
}

output "chaos_sns_topic_arn" {
  description = "ARN of the chaos SNS topic"
  value       = aws_sns_topic.chaos_notifications.arn
  sensitive   = false
}

output "chaos_efs_id" {
  description = "ID of the chaos EFS file system"
  value       = var.enable_storage_chaos ? aws_efs_file_system.chaos_efs[0].id : ""
  sensitive   = false
}

output "chaos_secret_arn" {
  description = "ARN of the chaos Secrets Manager secret"
  value       = aws_secretsmanager_secret.chaos_secret.arn
  sensitive   = false
}

output "chaos_parameter_name" {
  description = "Name of the chaos Parameter Store parameter"
  value       = aws_ssm_parameter.chaos_parameter.name
  sensitive   = false
}

output "chaos_ecs_cluster_arn" {
  description = "ARN of the chaos ECS cluster"
  value       = aws_ecs_cluster.chaos_cluster.arn
  sensitive   = false
}

output "chaos_alb_dns_name" {
  description = "DNS name of the chaos ALB"
  value       = var.enable_compute_chaos ? aws_lb.chaos_alb.dns_name : ""
  sensitive   = false
}

output "chaos_dynamodb_table_name" {
  description = "Name of the chaos DynamoDB table"
  value       = var.enable_storage_chaos ? aws_dynamodb_table.chaos_table[0].name : ""
  sensitive   = false
}

output "chaos_kinesis_stream_name" {
  description = "Name of the chaos Kinesis stream"
  value       = var.enable_compute_chaos ? aws_kinesis_stream.chaos_stream[0].name : ""
  sensitive   = false
}

output "chaos_state_machine_arn" {
  description = "ARN of the chaos Step Functions state machine"
  value       = var.enable_compute_chaos ? aws_sfn_state_machine.chaos_state_machine[0].arn : ""
  sensitive   = false
}

output "chaos_cloudtrail_name" {
  description = "Name of the chaos CloudTrail"
  value       = aws_cloudtrail.chaos_trail.name
  sensitive   = false
}

output "chaos_backup_vault_name" {
  description = "Name of the chaos Backup Vault"
  value       = var.enable_storage_chaos ? aws_backup_vault.chaos_backup_vault[0].name : ""
  sensitive   = false
}

output "chaos_waf_web_acl_id" {
  description = "ID of the chaos WAF Web ACL"
  value       = aws_wafv2_web_acl.chaos_waf.id
  sensitive   = false
}

output "chaos_api_gateway_id" {
  description = "ID of the chaos API Gateway"
  value       = var.enable_compute_chaos ? aws_api_gateway_rest_api.chaos_api[0].id : ""
  sensitive   = false
}

output "chaos_codecommit_repo_clone_url" {
  description = "Clone URL of the chaos CodeCommit repository"
  value       = var.enable_compute_chaos ? aws_codecommit_repository.chaos_repo[0].clone_url_http : ""
  sensitive   = false
}

output "chaos_codebuild_project_arn" {
  description = "ARN of the chaos CodeBuild project"
  value       = var.enable_compute_chaos ? aws_codebuild_project.chaos_build[0].arn : ""
  sensitive   = false
}

output "chaos_codepipeline_arn" {
  description = "ARN of the chaos CodePipeline"
  value       = var.enable_compute_chaos ? aws_codepipeline.chaos_pipeline[0].arn : ""
  sensitive   = false
}

output "chaos_event_rule_name" {
  description = "Name of the chaos EventBridge rule"
  value       = var.enable_compute_chaos ? aws_cloudwatch_event_rule.chaos_event_rule[0].name : ""
  sensitive   = false
}

output "chaos_glue_database_name" {
  description = "Name of the chaos Glue database"
  value       = var.enable_storage_chaos ? aws_glue_catalog_database.chaos_glue_db[0].name : ""
  sensitive   = false
}

output "chaos_glue_table_name" {
  description = "Name of the chaos Glue table"
  value       = var.enable_storage_chaos ? aws_glue_catalog_table.chaos_glue_table[0].name : ""
  sensitive   = false
}

output "chaos_athena_workgroup_name" {
  description = "Name of the chaos Athena workgroup"
  value       = var.enable_storage_chaos ? aws_athena_workgroup.chaos_athena_wg[0].name : ""
  sensitive   = false
}

output "chaos_redshift_cluster_id" {
  description = "ID of the chaos Redshift cluster"
  value       = var.enable_storage_chaos && var.chaos_level == "high" ? aws_redshift_cluster.chaos_redshift[0].id : ""
  sensitive   = false
}

output "chaos_sqs_queue_url" {
  description = "URL of the chaos SQS queue"
  value       = var.enable_compute_chaos ? aws_sqs_queue.chaos_queue[0].id : ""
  sensitive   = false
}

output "chaos_cloudformation_stack_id" {
  description = "ID of the chaos CloudFormation stack"
  value       = var.enable_compute_chaos ? aws_cloudformation_stack.chaos_cf_stack[0].id : ""
  sensitive   = false
}

output "chaos_cloudformation_stackset_id" {
  description = "ID of the chaos CloudFormation stack set"
  value       = var.enable_compute_chaos ? aws_cloudformation_stack_set.chaos_cf_stackset[0].id : ""
  sensitive   = false
}

output "chaos_garden_tags" {
  description = "Tags applied to all chaos garden resources"
  value       = merge(
    {
      chaos_garden = "true"
      environment  = var.environment
      chaos_level  = var.chaos_level
      terraform    = "true"
    },
    var.tags
  )
  sensitive   = false
}

output "chaos_garden_summary" {
  description = "Summary of all chaos garden resources"
  value       = {
    garden_name           = local.chaos_name
    vpc_id               = aws_vpc.chaos_vpc.id
    subnet_ids           = aws_subnet.chaos_subnets[*].id
    security_group_id    = aws_security_group.chaos_sg.id
    instance_ids         = var.enable_compute_chaos ? aws_instance.chaos_instances[*].id : []
    bucket_names         = var.enable_storage_chaos ? aws_s3_bucket.chaos_buckets[*].id : []
    rds_endpoint         = var.enable_compute_chaos && var.chaos_level == "high" ? aws_db_instance.chaos_rds[0].endpoint : ""
    lambda_arn           = var.enable_compute_chaos ? aws_lambda_function.chaos_lambda[0].arn : ""
    sns_topic_arn        = aws_sns_topic.chaos_notifications.arn
    efs_id               = var.enable_storage_chaos ? aws_efs_file_system.chaos_efs[0].id : ""
    secret_arn           = aws_secretsmanager_secret.chaos_secret.arn
    parameter_name       = aws_ssm_parameter.chaos_parameter.name
    ecs_cluster_arn      = aws_ecs_cluster.chaos_cluster.arn
    alb_dns_name         = var.enable_compute_chaos ? aws_lb.chaos_alb.dns_name : ""
    dynamodb_table_name  = var.enable_storage_chaos ? aws_dynamodb_table.chaos_table[0].name : ""
    kinesis_stream_name  = var.enable_compute_chaos ? aws_kinesis_stream.chaos_stream[0].name : ""
    state_machine_arn    = var.enable_compute_chaos ? aws_sfn_state_machine.chaos_state_machine[0].arn : ""
    cloudtrail_name      = aws_cloudtrail.chaos_trail.name
    backup_vault_name    = var.enable_storage_chaos ? aws_backup_vault.chaos_backup_vault[0].name : ""
    waf_web_acl_id       = aws_wafv2_web_acl.chaos_waf.id
    api_gateway_id       = var.enable_compute_chaos ? aws_api_gateway_rest_api.chaos_api[0].id : ""
    codecommit_repo_url  = var.enable_compute_chaos ? aws_codecommit_repository.chaos_repo[0].clone_url_http : ""
    codebuild_project_arn = var.enable_compute_chaos ? aws_codebuild_project.chaos_build[0].arn : ""
    codepipeline_arn     = var.enable_compute_chaos ? aws_codepipeline.chaos_pipeline[0].arn : ""
    event_rule_name      = var.enable_compute_chaos ? aws_cloudwatch_event_rule.chaos_event_rule[0].name : ""
    glue_database_name   = var.enable_storage_chaos ? aws_glue_catalog_database.chaos_glue_db[0].name : ""
    glue_table_name      = var.enable_storage_chaos ? aws_glue_catalog_table.chaos_glue_table[0].name : ""
    athena_workgroup_name = var.enable_storage_chaos ? aws_athena_workgroup.chaos_athena_wg[0].name : ""
    redshift_cluster_id  = var.enable_storage_chaos && var.chaos_level == "high" ? aws_redshift_cluster.chaos_redshift[0].id : ""
    sqs_queue_url        = var.enable_compute_chaos ? aws_sqs_queue.chaos_queue[0].id : ""
    cloudformation_stack_id = var.enable_compute_chaos ? aws_cloudformation_stack.chaos_cf_stack[0].id : ""
    cloudformation_stackset_id = var.enable_compute_chaos ? aws_cloudformation_stack_set.chaos_cf_stackset[0].id : ""
  }
  sensitive   = false
}
