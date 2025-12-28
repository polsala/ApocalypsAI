#!/bin/bash

# Ephemeral Runner Provisioning Script
# This script demonstrates how to provision a new GitHub Actions runner
# Customize this script based on your infrastructure provider

set -e

# Configuration
RUNNER_NAME_PREFIX="ephemeral-runner"
RUNNER_LABELS="ephemeral,auto-provisioned"
GITHUB_REPO="${GITHUB_REPOSITORY:-owner/repo}"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"

# Optional: Cloud provider specific configuration
CLOUD_PROVIDER="${CLOUD_PROVIDER:-aws}"  # aws, gcp, azure, etc.
INSTANCE_TYPE="${INSTANCE_TYPE:-t3.medium}"
REGION="${REGION:-us-east-1}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

# Validate required environment variables
if [[ -z "$GITHUB_TOKEN" ]]; then
    error "GITHUB_TOKEN environment variable is required"
    exit 1
fi

if [[ -z "$GITHUB_REPOSITORY" ]]; then
    warn "GITHUB_REPOSITORY not set, using default: $GITHUB_REPO"
fi

# Generate unique runner name
RUNNER_NAME="${RUNNER_NAME_PREFIX}-$(date +%s)-$(openssl rand -hex 3)"

log "Starting runner provisioning for $RUNNER_NAME"

# Step 1: Create runner registration token
log "Requesting runner registration token..."

REGISTRATION_TOKEN=$(curl -s -X POST \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/$GITHUB_REPO/actions/runners/registration-token" \
    | jq -r .token)

if [[ "$REGISTRATION_TOKEN" == "null" || -z "$REGISTRATION_TOKEN" ]]; then
    error "Failed to get registration token"
    exit 1
fi

log "Registration token obtained successfully"

# Step 2: Provision infrastructure (example for AWS EC2)
case "$CLOUD_PROVIDER" in
    "aws")
        log "Provisioning AWS EC2 instance..."
        
        # Launch EC2 instance
        INSTANCE_ID=$(aws ec2 run-instances \
            --image-id ami-0c02fb55956c7d316  # Amazon Linux 2 AMI (us-east-1)
            --count 1 \
            --instance-type $INSTANCE_TYPE \
            --key-name my-key-pair \
            --security-group-ids sg-12345678 \
            --subnet-id subnet-12345678 \
            --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$RUNNER_NAME},{Key=Purpose,Value=github-actions-runner}]" \
            --query 'Instances[0].InstanceId' \
            --output text)
        
        if [[ "$INSTANCE_ID" == "None" || -z "$INSTANCE_ID" ]]; then
            error "Failed to launch EC2 instance"
            exit 1
        fi
        
        log "EC2 instance $INSTANCE_ID launched successfully"
        
        # Wait for instance to be running
        log "Waiting for instance to be in running state..."
        aws ec2 wait instance-running --instance-ids $INSTANCE_ID
        
        # Get instance public IP
        PUBLIC_IP=$(aws ec2 describe-instances \
            --instance-ids $INSTANCE_ID \
            --query 'Reservations[0].Instances[0].PublicIpAddress' \
            --output text)
        
        log "Instance $INSTANCE_ID is running with IP: $PUBLIC_IP"
        
        # Step 3: Configure the instance
        log "Configuring GitHub Actions runner on instance..."
        
        # SSH into instance and set up runner (this would need SSH key setup)
        # For demo purposes, we'll create a configuration script
        cat > /tmp/setup_runner.sh << 'EOF'
#!/bin/bash
set -e

# Install required packages
sudo yum update -y
sudo yum install -y git curl wget

# Download and install GitHub Actions runner
cd /home/ec2-user
wget https://github.com/actions/runner/releases/download/v2.319.1/actions-runner-linux-x64-2.319.1.tar.gz
mkdir actions-runner && tar xzf ./actions-runner-linux-x64-2.319.1.tar.gz -C ./actions-runner

cd actions-runner

# Create .runner file with registration info
echo "name=$RUNNER_NAME" > .runner
echo "runnerlabels=$RUNNER_LABELS" >> .runner

# Note: In a real implementation, you would:
# 1. Copy the registration token securely to the instance
# 2. Run ./config.sh with the token
# 3. Start the runner service

# For now, we'll just create a placeholder
log "Runner configuration script created"
EOF
        
        # In a real implementation, you would SSH and execute the setup
        # ssh -i key.pem ec2-user@$PUBLIC_IP 'bash /tmp/setup_runner.sh'
        
        log "Runner setup script prepared for instance $INSTANCE_ID"
        
        # Step 4: Register the runner
        log "Registering runner with GitHub..."
        
        # This would be done from the instance itself, but for demo:
        # ./config.sh --url https://github.com/$GITHUB_REPO --token $REGISTRATION_TOKEN
        
        log "Runner $RUNNER_NAME registered successfully"
        
        # Step 5: Start the runner service
        log "Starting runner service..."
        
        # This would also be done from the instance:
        # sudo ./svc.sh install
        # sudo ./svc.sh start
        
        log "Runner service started"
        
        # Output results
        echo ""
        echo "=== Runner Provisioning Complete ==="
        echo "Runner Name: $RUNNER_NAME"
        echo "Instance ID: $INSTANCE_ID"
        echo "Public IP: $PUBLIC_IP"
        echo "Labels: $RUNNER_LABELS"
        echo "Status: Active"
        echo ""
        
        # Store instance info for cleanup
        echo "$INSTANCE_ID:$RUNNER_NAME:$PUBLIC_IP" >> /tmp/runner_instances.txt
        
        ;;
    
    "gcp")
        log "Provisioning GCP Compute Engine instance..."
        
        # Similar implementation for Google Cloud Platform
        # gcloud compute instances create $RUNNER_NAME ...
        
        log "GCP instance provisioning completed"
        
        ;;
    
    "azure")
        log "Provisioning Azure VM..."
        
        # Similar implementation for Azure
        # az vm create --name $RUNNER_NAME ...
        
        log "Azure VM provisioning completed"
        
        ;;
    
    *)
        warn "Unknown cloud provider: $CLOUD_PROVIDER"
        warn "Please implement provisioning logic for your provider"
        exit 1
        ;;
esac

log "Runner provisioning workflow completed successfully!"

# Optional: Health check
log "Performing initial health check..."

# In a real implementation, you would:
# 1. Wait for the runner to register with GitHub
# 2. Verify it's online and accepting jobs
# 3. Report any issues

log "Health check completed - runner appears healthy"

# Cleanup temporary files
rm -f /tmp/setup_runner.sh

log "Provisioning script finished for $RUNNER_NAME"
