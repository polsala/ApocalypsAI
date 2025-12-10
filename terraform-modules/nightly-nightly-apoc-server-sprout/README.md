# Apocalyptic Server Sprout

A Terraform module to deploy a cluster of survival-themed servers with playful tags like 'Water Purifier', 'Radiation Shield', and 'Wasteland Beacon'.

## Variables
- `region`: Cloud region for deployment
- `instance_type`: VM size (default: t2.micro)
- `survival_role`: Server purpose (e.g. 'Water Purifier')

## Example
```terraform
module "sprout" {
  source = "./nightly-apoc-server-sprout"
  region = "us-west-2"
  survival_role = "Radiation Shield"
}
```
