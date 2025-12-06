# Doomsday Device Config Validator

## 💥 Ensure Your Apocalypse Plans Are Flawless! 💥

This utility, the `doomsday-config-validator`, is your last line of defense against a poorly configured global cataclysm (or, you know, a regular software deployment). It's a whimsical yet genuinely useful tool designed to validate your critical JSON or YAML configuration files, ensuring they are syntactically correct and contain all the essential parameters for your world-ending (or world-saving) operations.

No more accidental `null` values where a `true` was needed for the self-destruct sequence! No more missing `target_coordinates` for your orbital laser! This validator ensures your doomsday device (or microservice) configurations are robust.

## How to Use

1.  **Install dependencies (if using YAML):**
    ```bash
    pip install PyYAML
    ```
2.  **Run the validator:**
    ```bash
    python src/validator.py <path_to_config_file> [--required-keys KEY1 KEY2 ...] [--type json|yaml]
    ```

    *   `<path_to_config_file>`: The path to the configuration file you want to validate.
    *   `--required-keys`: A space-separated list of top-level keys that *must* be present in the configuration.
    *   `--type`: Explicitly specify the file type (`json` or `yaml`). If omitted, it attempts to guess based on file extension.

## Examples

### Validating a JSON file with required keys:

```bash
python src/validator.py configs/launch_sequence.json --required-keys activation_code target_system
```

### Validating a YAML file for syntax only:

```bash
python src/validator.py configs/bunker_layout.yaml --type yaml
```

## Exit Codes

*   `0`: Configuration is valid.
*   `1`: Configuration is invalid (syntax error, missing keys, or file not found).
