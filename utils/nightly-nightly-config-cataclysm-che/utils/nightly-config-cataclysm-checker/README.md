# Nightly Config Cataclysm Checker

## 🚨 Prevent Configuration Cataclysms! 🚨

The `nightly-config-cataclysm-checker` is a whimsical-yet-critical utility designed to ensure your project's local environment and deployment configurations are always in tip-top shape. Before a minor misconfiguration escalates into a full-blown "cataclysm" of broken builds and frustrated developers, this checker will scan for missing files, incorrect directory structures, and improperly set environment variables.

It's like a pre-apocalyptic warning system for your project's setup!

## ✨ Features

*   **Configurable Checks**: Define required files, directories, and environment variables using a simple JSON specification file.
*   **File Type Validation**: Automatically checks if files are valid JSON or YAML.
*   **Environment Variable Type Validation**: Ensures environment variables conform to expected types (string, int, boolean).
*   **Clear Reporting**: Provides a concise list of all detected issues, helping you pinpoint and resolve problems quickly.
*   **Whimsical Naming**: Because even impending doom can be fun!

## 🚀 Usage

1.  **Create a Specification File**:
    First, create a JSON file (e.g., `config_spec.json`) that outlines your project's required configurations.

    ```json
    {
      "files": [
        {
          "path": "config/app_settings.json",
          "required": true,
          "type": "json",
          "description": "Main application configuration file."
        },
        {
          "path": "data/",
          "required": true,
          "type": "directory",
          "description": "Directory for application data."
        },
        {
          "path": "logs/debug.log",
          "required": false,
          "type": "file",
          "description": "Optional debug log file."
        },
        {
          "path": "credentials.yaml",
          "required": true,
          "type": "yaml",
          "description": "Sensitive credentials (ensure proper permissions!)."
        }
      ],
      "env_vars": [
        {
          "name": "API_KEY",
          "required": true,
          "type": "string",
          "description": "API key for external service."
        },
        {
          "name": "DEBUG_MODE",
          "required": false,
          "type": "boolean",
          "description": "Enable debug logging (true/false/1/0)."
        },
        {
          "name": "MAX_CONNECTIONS",
          "required": true,
          "type": "int",
          "description": "Maximum number of database connections."
        }
      ]
    }
    ```

    **`files` properties**:
    *   `path` (string, **required**): The path to the file or directory.
    *   `required` (boolean, optional, default `true`): If `false`, its absence won't cause an error.
    *   `type` (string, optional, default `file`): Can be `file`, `directory`, `json`, or `yaml`.
    *   `description` (string, optional): A human-readable description.

    **`env_vars` properties**:
    *   `name` (string, **required**): The name of the environment variable.
    *   `required` (boolean, optional, default `true`): If `false`, its absence won't cause an error.
    *   `type` (string, optional, default `string`): Can be `string`, `int`, or `boolean`.
    *   `description` (string, optional): A human-readable description.

2.  **Run the Checker**:
    Execute the `checker.py` script, providing the path to your specification file.

    ```bash
    python src/checker.py config_spec.json
    ```

    *   If all checks pass, it will exit with code `0` and a success message.
    *   If any issues are found, it will exit with code `1` and list all detected "cataclysms."

## 🧪 Development & Testing

To run the tests for this utility:

```bash
python -m unittest tests/test_checker.py
```

The tests are designed to be deterministic and offline, using Python's `unittest.mock` to simulate file system interactions and environment variables.
