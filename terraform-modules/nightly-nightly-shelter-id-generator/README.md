Nightly Shelter ID Generator Terraform Module

A whimsical Terraform module that creates a unique shelter ID using the random_id resource. Perfect for post‑apocalyptic infrastructure where every safehouse needs a distinct identifier.

Features
- Generates a random, URL‑safe ID of configurable length.
- Accepts a custom shelter name and capacity.
- Outputs the generated ID and a formatted shelter tag.

Usage
module "shelter_id" {
  source        = "./nightly-shelter-id-generator"
  shelter_name  = "Wasteland Haven"
  capacity      = 42
  id_length     = 8
}

Inputs
Name          Description                                 Type    Default
shelter_name  Human‑readable name of the shelter           string  "Unnamed Shelter"
capacity      Maximum number of occupants                 number  10
id_length     Length of the random ID (bytes)              number  8

Outputs
Name        Description
shelter_id  The generated random ID
shelter_tag Formatted tag: <shelter_name>-<shelter_id>

Testing
Run the provided test script:
cd tests && ./validate.sh
The script runs terraform init and terraform validate using the null provider, ensuring deterministic results offline.

License
MIT
