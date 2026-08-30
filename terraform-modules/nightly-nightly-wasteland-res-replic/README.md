# Nightly Wasteland Resource Replicator

## Overview

The `nightly-wasteland-res-replicat` Terraform module is designed to bring order to the chaotic post-apocalyptic cloud landscape. It ensures that your critical 'survival outposts' (cloud resources) are automatically replicated and maintained at a desired count, acting as a self-healing mechanism against unexpected 'wasteland anomalies' (resource deletion, configuration drift, or general digital decay).

This module is ideal for maintaining a resilient baseline of essential infrastructure components, ensuring that even if a 'temporal distortion' wipes out a resource, a replacement is swiftly provisioned.

## Features

*   **Automated Replication**: Define a desired count, and the module ensures that many instances of your specified resource type exist.
*   **Self-Healing**: If resources are unexpectedly removed, a `terraform apply` will bring them back to the desired state.
*   **Configurable**: Easily adjust the type and count of resources to be replicated.
*   **Whimsical Theming**: Integrates seamlessly into the ApocalypsAI universe with its 'wasteland' and 'temporal' concepts.

## Usage

To use this module, include it in your Terraform configuration and provide the required variables.

```terraform
module "survival_outposts" {
  source = "./modules/nightly-wasteland-res-replicat/src" # Adjust path as necessary

  resource_type  = "data_cache_node" # e.g., "survival_pod", "generator_unit"
  resource_count = 5                 # Ensure 5 data cache nodes are always present
}

output "outpost_ids" {
  value = module.survival_outposts.replicated_resource_ids
}
```

## Module Inputs

| Name            | Description                                                               | Type   | Default          | Required |
|-----------------|---------------------------------------------------------------------------|--------|------------------|----------|
| `resource_type` | The type of resource to replicate (e.g., 'survival_pod', 'data_cache').   | `string` | `"survival_pod"` | no       |
| `resource_count`| The desired number of replicated resources. Must be greater than 0.       | `number` | `3`              | no       |

## Module Outputs

| Name                      | Description                                         | Value Type |
|---------------------------|-----------------------------------------------------|------------|
| `replicated_resource_ids` | A list of identifiers for the replicated resources. | `list(string)` |

## Testing

Refer to the `tests/` directory for an example of how to validate this module locally using `terraform validate`.
