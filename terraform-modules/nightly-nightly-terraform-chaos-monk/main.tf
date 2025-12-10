terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "random" {}

# Random number generator for chaos probability
resource "random_integer" "chaos_roll" {
  count  = var.enable_chaos ? 1 : 0
  min    = 1
  max    = 100
  result = random_integer.chaos_roll[0].result
}

# Chaos monkey execution logic
resource "null_resource" "chaos_monkey" {
  count = var.enable_chaos ? 1 : 0
  
  triggers = {
    chaos_probability = var.chaos_probability
    timestamp         = timestamp()
  }
  
  provisioner "local-exec" {
    when    = destroy
    on_failure = continue
    command = <<-EOT
      #!/bin/bash
      
      # ASCII art chaos monkey
      cat << 'MONKEY_EOF'
      ${data.template_file.chaos_monkey_ascii.rendered}
      MONKEY_EOF
      
      echo ""
      echo "=== CHAOS MONKEY REPORT ==="
      echo "Timestamp: $(date)"
      echo "Monkey Mood: ${data.random_string.monkey_mood.result}"
      echo "Chaos Probability: ${var.chaos_probability}"
      echo "Rolled: ${random_integer.chaos_roll[0].result}"
      echo ""
      
      # Check if chaos should happen
      if [ ${random_integer.chaos_roll[0].result} -le $(( ${var.chaos_probability} * 100 )) ]; then
        echo "🎉 CHAOS TIME! The monkey is feeling mischievous!"
        echo ""
        
        # Get list of target resources
        TARGET_RESOURCES=$(aws ec2 describe-instances \
          --filters "Name=tag:Environment,Values=${var.target_environment}" \
          --query 'Reservations[].Instances[?State.Name==`running`].InstanceId' \
          --output text)
        
        if [ -z "$TARGET_RESOURCES" ]; then
          echo "No target resources found. The monkey is disappointed but will wait."
        else
          # Select random resource to terminate
          RESOURCE_LIST=($TARGET_RESOURCES)
          RANDOM_INDEX=$((RANDOM % ${#RESOURCE_LIST[@]}))
          TARGET_RESOURCE=${RESOURCE_LIST[$RANDOM_INDEX]}
          
          echo "🎯 Target selected: $TARGET_RESOURCE"
          
          # Safety check - verify it's not excluded
          EXCLUDED=$(aws ec2 describe-tags \
            --filters "Name=resource-id,Values=$TARGET_RESOURCE" \
            --query 'Tags[?Key==`${var.exclusion_tag_key}` && Value==`${var.exclusion_tag_value}`].Value' \
            --output text)
          
          if [ "$EXCLUDED" = "${var.exclusion_tag_value}" ]; then
            echo "⚠️  Resource is excluded from chaos. Skipping."
          else
            echo "💥 Executing chaos on $TARGET_RESOURCE"
            
            # Terminate the instance
            aws ec2 terminate-instances --instance-ids $TARGET_RESOURCE
            
            if [ $? -eq 0 ]; then
              echo "🎉 Success! $TARGET_RESOURCE has been terminated by chaos monkey."
              echo ""
              echo "${data.template_file.chaos_quotes.rendered}"
            else
              echo "❌ Failed to terminate $TARGET_RESOURCE. The monkey is angry!"
            fi
          fi
        fi
      else
        echo "😌 Safe day! The monkey is napping. No chaos today."
        echo ""
        echo "${data.template_file.chaos_quotes.rendered}"
      fi
      
      echo ""
      echo "=== END REPORT ==="
    EOT
  }
}

# Monkey mood generator
resource "random_string" "monkey_mood" {
  length  = 6
  upper   = false
  special = false
  result  = random_string.monkey_mood.result
}

# Data sources for templates
data "template_file" "chaos_monkey_ascii" {
  template = <<-EOT
    🐒  CHAOS MONKEY  🐒
    🍌  Ready for mayhem!  🍌
    
       ,#####,
       #_   _#
       |a` `a|
       |  u  |
       \  _  /
        |@ @|
        |   |
        |   |
        |   |
        |   |
        |   |
        |   |
        |   |
        |   |
        |   |
        'ccc'
    EOT
}

data "template_file" "chaos_quotes" {
  template = <<-EOT
    "${random_string.chaos_quote.result}"
    
    Remember: With great chaos comes great responsibility!
    (And possibly some angry developers...)
  EOT
}

# Random chaos quotes
resource "random_string" "chaos_quote" {
  length  = 1
  upper   = false
  special = false
  result  = lookup({
    "0" = "Chaos isn't a pit. Chaos is a ladder."
    "1" = "The only way to survive chaos is to become chaos."
    "2" = "In chaos, there is opportunity."
    "3" = "Mayhem is just another word for freedom!"
    "4" = "The monkey always wins in the end."
    "5" = "Embrace the chaos, for it is life!"
    "6" = "Sometimes you have to break things to make them better."
    "7" = "Chaos is the spice of cloud infrastructure!"
    "8" = "What doesn't kill your infrastructure makes it stronger."
    "9" = "The best time to plant a tree was 20 years ago. The second best time is to terminate an instance and watch your auto-scaling handle it."
  }, random_string.chaos_quote.result, "Chaos is what we'll become!")
}

# Output the chaos report
output "chaos_report" {
  value = <<-EOT
    Chaos Monkey Report:
    - Enabled: ${var.enable_chaos}
    - Probability: ${var.chaos_probability}
    - Environment: ${var.target_environment}
    - Last Roll: ${random_integer.chaos_roll[0].result}
    - Monkey Mood: ${random_string.monkey_mood.result}
  EOT
  sensitive = false
}
