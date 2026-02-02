#!/bin/bash
set -euo pipefail

# Whimsical intro
echo "--- Ephemeral Beacon Activated ---"
echo "Initiating Wasteland Scout Protocol..."

# Log file setup
LOG_FILE="/var/log/beacon_task.log"
exec > >(tee -a $LOG_FILE) 2>&1

echo "Beacon ID: $$(hostname)"
echo "Starting task at $$(date)"
echo "Task script: ${task_script}"

# User-provided task script
eval "${task_script}"

TASK_EXIT_CODE=$$?
echo "Task completed with exit code: $TASK_EXIT_CODE at $$(date)"

# Optional: Upload logs to S3
if [ -n "${log_bucket_name}" ] && [ "${log_bucket_name}" != "null" ]; then
    echo "Uploading logs to s3://${log_bucket_name}/beacon_logs/$$(hostname)-$$(date +%Y%m%d%H%M%S).log"
    aws s3 cp "$LOG_FILE" "s3://${log_bucket_name}/beacon_logs/$$(hostname)-$$(date +%Y%m%d%H%M%S).log" --region "${region}"
    S3_UPLOAD_EXIT_CODE=$$?
    if [ $$S3_UPLOAD_EXIT_CODE -ne 0 ]; then
        echo "Failed to upload logs to S3. AWS CLI exit code: $$S3_UPLOAD_EXIT_CODE"
    else
        echo "Logs uploaded successfully."
    fi
fi

# Optional: Self-terminate
if [ "${self_terminate}" == "true" ]; then
    echo "Self-termination protocol initiated."
    INSTANCE_ID=$$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
    echo "Terminating instance $$INSTANCE_ID..."
    aws ec2 terminate-instances --instance-ids "$$INSTANCE_ID" --region "${region}"
    echo "Termination command sent for $$INSTANCE_ID."
else
    echo "Beacon will remain active. Remember to terminate it manually if not needed."
fi

echo "--- Ephemeral Beacon Deactivated ---"
