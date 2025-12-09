# Test runner for chaos orchestrator
.PHONY: test clean init plan apply destroy

# Initialize Terraform
init:
	terraform init

# Run Terraform plan
plan:
	terraform plan -out=plan.out

# Apply Terraform configuration
apply:
	terraform apply plan.out

# Destroy created resources
destroy:
	terraform destroy -auto-approve

# Clean up test files
clean:
	rm -f plan.out terraform.tfstate terraform.tfstate.backup

# Run full test cycle
test: init plan apply destroy clean
	@echo "Chaos orchestrator tests completed successfully!"
