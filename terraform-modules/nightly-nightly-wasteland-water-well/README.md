# Wasteland Water Well Module

A Terraform module to create virtual water wells with configurable quotas and alerts. Perfect for simulating resource management in post-apocalyptic scenarios or real-world cloud resource quotas.

## Usage

```hcl
module "water_well" {
  source = "./wasteland-water-well"

  well_name = "oasis-1"
  capacity_liters = 1000
  alert_threshold = 200
}
```

## Variables
- `well_name`: Name of the water well
- `capacity_liters`: Maximum storage capacity
- `alert_threshold`: Liters remaining to trigger alerts

## Outputs
- `well_status`: Current status summary
- `remaining_water`: Available liters
