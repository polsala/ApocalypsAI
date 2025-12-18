# Nightly Digital Bottle Post

## Summary
This Terraform module provisions a secure, globally accessible AWS S3 bucket, acting as a 'Digital Message in a Bottle'. It allows survivors to broadcast vital (or whimsical) messages across the digital wasteland, ensuring resilience and wide reach.

## Whimsical Utility
In a world where traditional communication infrastructure might be compromised, this module provides a resilient, cloud-based platform to leave messages for others. Whether it's a warning about a temporal anomaly, a recipe for mutated squirrel stew, or just a hopeful greeting, your message will persist and be accessible to anyone who finds your digital bottle.

## Usage
To use this module, include it in your Terraform configuration and provide the required variables. Ensure you have AWS credentials configured for Terraform.

```terraform
module "my_message_bottle" {
  source = "./path/to/nightly-digital-bottle-post/src"

  bucket_name     = "your-unique-bottle-name-$(random_id.suffix.hex)" # Must be globally unique
  message_content = "Beware the glowing rad-rabbits near Sector 7!"
  public_read     = true # Set to false for a private message bottle
}

resource "random_id" "suffix" {
  byte_length = 8
}

output "bottle_url" {
  value = module.my_message_bottle.initial_message_url
}
```

### Inputs

*   `bucket_name` (string, Required): The name for the S3 bucket. **Must be globally unique.**
*   `message_content` (string, Optional): The initial message content to place in the bottle. Defaults to "Greetings, fellow survivors! May this message find you well. - ApocalypsAI".
*   `public_read` (bool, Optional): Set to `true` to make the bucket and its initial message publicly readable. Use with caution. Defaults to `true`.

### Outputs

*   `bucket_endpoint`: The HTTP endpoint for the S3 bucket.
*   `initial_message_url`: The URL to the initial message object.

## Testing

To run the automated tests, navigate to the `tests/` directory and execute the `run_tests.sh` script. This script performs offline validation and planning checks without provisioning actual cloud resources.

```bash
cd tests/
bash run_tests.sh
```
