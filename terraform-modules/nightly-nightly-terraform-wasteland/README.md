# Nightly Terraform Wasteland Terraform Module

A whimsical-yet-practical Terraform module generator for creating post-apocalyptic infrastructure resources with survival-themed naming conventions.

## Features

- Generates survival-themed resource names (e.g., `wasteland-water-tank`, `scavenger-storage-bucket`)
- Creates realistic disaster recovery configurations
- Includes survival-themed variables and outputs
- Provides example configurations for different apocalypse scenarios

## Usage

```hcl
module "wasteland_infrastructure" {
  source = "./modules/nightly-terraform-wasteland-terraform"
  
  # Basic configuration
  region = "us-east-1"
  environment = "post-apocalypse"
  
  # Survival resources
  water_tanks = 3
  food_stores = 5
  power_generators = 2
  
  # Security measures
  perimeter_fencing = true
  watch_towers = 4
  
  # Communication
  radio_towers = 2
  emergency_frequency = "101.5MHz"
}
```

## Variables

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `region` | AWS region for resources | string | "us-east-1" |
| `environment` | Environment name | string | "post-apocalypse" |
| `water_tanks` | Number of water storage tanks | number | 1 |
| `food_stores` | Number of food storage facilities | number | 1 |
| `power_generators` | Number of backup power generators | number | 1 |
| `perimeter_fencing` | Enable perimeter security | bool | false |
| `watch_towers` | Number of security watch towers | number | 0 |
| `radio_towers` | Number of communication towers | number | 1 |
| `emergency_frequency` | Emergency radio frequency | string | "101.5MHz" |

## Outputs

| Output | Description |
|--------|-------------|
| `survival_resources` | Map of created survival resources |
| `security_perimeter` | Security configuration details |
| `communication_nodes` | Communication infrastructure details |
| `total_survival_score` | Calculated survival readiness score |

## Example Scenarios

### Zombie Outbreak
```hcl
module "zombie_outbreak" {
  source = "./modules/nightly-terraform-wasteland-terraform"
  
  environment = "zombie-outbreak"
  water_tanks = 10
  food_stores = 15
  power_generators = 5
  perimeter_fencing = true
  watch_towers = 8
  radio_towers = 3
}
```

### Nuclear Winter
```hcl
module "nuclear_winter" {
  source = "./modules/nightly-terraform-wasteland-terraform"
  
  environment = "nuclear-winter"
  water_tanks = 20
  food_stores = 30
  power_generators = 10
  perimeter_fencing = true
  watch_towers = 12
  radio_towers = 5
  emergency_frequency = "98.7MHz"
}
```

## License

MIT - Use to build your bunker, not to destroy it.
