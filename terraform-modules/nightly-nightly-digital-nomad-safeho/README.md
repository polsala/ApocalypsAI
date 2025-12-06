Digital Nomad Safehouse
=======================

A Terraform module that creates a secure network environment with:
- Private VPC with isolated subnets
- Bastion host with SSH access control
- Web server with HTTPS termination
- Auto-scaling group for redundancy

Usage:
1. Configure variables in `terraform.tfvars`
2. Run `terraform apply`
3. Access the web dashboard at `https://<output_url>`

Security features include automatic TLS certificate renewal, network ACLs, and IAM role-based access control.
