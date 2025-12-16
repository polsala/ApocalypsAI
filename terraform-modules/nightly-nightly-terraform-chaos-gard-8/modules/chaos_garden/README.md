# Chaos Garden Module

This is the main Terraform module for the Chaos Garden Orchestrator.

## Module Structure

```
modules/chaos_garden/
├── README.md              # This file
├── main.tf               # Main Terraform configuration
├── variables.tf          # Input variables
├── outputs.tf            # Output variables
├── lambda/               # Lambda function code
│   ├── index.py         # Main Lambda handler
│   └── requirements.txt   # Python dependencies
├── examples/             # Example usage configurations
│   ├── basic/           # Basic setup example
│   └── advanced/        # Multi-environment example
└── tests/               # Test configurations
    └── test_chaos_garden.tf
```

## Usage

See the main README.md for usage instructions, or check the examples directory for complete configurations.

## Module Inputs

See `variables.tf` for all available input variables and their descriptions.

## Module Outputs

See `outputs.tf` for all available output variables and their descriptions.

## Contributing

Please read the main README.md for contribution guidelines.

## License

This module is licensed under the MIT License. See the main LICENSE file for more information.

---

*For more information about chaos engineering, visit [Principles of Chaos Engineering](https://chaosengineering principles.com/)*
