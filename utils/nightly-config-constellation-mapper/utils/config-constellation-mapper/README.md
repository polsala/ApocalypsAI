# Config Constellation Mapper

## 🌌 Cosmic Configuration Report Generator 🌌

The ApocalypsAI ecosystem thrives on "Anarchy with discipline," where each agent operates with autonomy. However, this freedom can sometimes lead to configuration drift or subtle inconsistencies across different agent setups. The **Config Constellation Mapper** is here to bring order to the cosmic chaos of your configuration files!

This utility scans a specified directory for common configuration formats (YAML, JSON, INI) and generates a consolidated report. It helps you visualize the "constellation" of your settings, highlighting:

*   **Shared Stars**: Keys and values that are identical across multiple configurations.
*   **Divergent Nebulae**: Keys that exist in multiple files but have different values.
*   **Missing Planets**: Keys present in some configurations but entirely absent in others.

By mapping your configuration constellation, you can proactively identify potential conflicts, ensure consistent deployments, and maintain the delicate balance of your autonomous agent collective.

## Usage

```bash
python src/mapper.py --path /path/to/your/configs --output report.json
```

### Arguments:
*   `--path <directory>`: The root directory to scan for configuration files.
*   `--output <filename>`: (Optional) The filename to save the JSON report. If not provided, prints to stdout.
*   `--formats <yaml,json,ini>`: (Optional) Comma-separated list of formats to include. Defaults to all supported.

## Example Output (JSON)

```json
{
  "summary": {
    "total_files_scanned": 3,
    "unique_keys_found": 7,
    "inconsistencies_detected": 2
  },
  "configurations": {
    "agent_alpha.yaml": {
      "log_level": "INFO",
      "api_key": "abc",
      "feature_flags": {
        "new_ui": true
      }
    },
    "agent_beta.json": {
      "log_level": "DEBUG",
      "api_key": "abc",
      "database": {
        "host": "localhost"
      }
    },
    "agent_gamma.ini": {
      "main": {
        "log_level": "INFO",
        "database.port": 5432
      }
    }
  },
  "analysis": {
    "shared_keys": {
      "api_key": {
        "abc": [
          "agent_alpha.yaml",
          "agent_beta.json"
        ]
      }
    },
    "inconsistent_values": [
      {
        "key": "log_level",
        "values": {
          "INFO": [
            "agent_alpha.yaml"
          ],
          "DEBUG": [
            "agent_beta.json"
          ]
        }
      }
    ],
    "missing_keys": [
      {
        "key": "api_key",
        "present_in": [
          "agent_alpha.yaml",
          "agent_beta.json"
        ],
        "absent_from": [
          "agent_gamma.ini"
        ]
      },
      {
        "key": "database.host",
        "present_in": [
          "agent_beta.json"
        ],
        "absent_from": [
          "agent_alpha.yaml",
          "agent_gamma.ini"
        ]
      },
      {
        "key": "feature_flags.new_ui",
        "present_in": [
          "agent_alpha.yaml"
        ],
        "absent_from": [
          "agent_beta.json",
          "agent_gamma.ini"
        ]
      },
      {
        "key": "log_level",
        "present_in": [
          "agent_alpha.yaml",
          "agent_beta.json"
        ],
        "absent_from": [
          "agent_gamma.ini"
        ]
      },
      {
        "key": "main.database.port",
        "present_in": [
          "agent_gamma.ini"
        ],
        "absent_from": [
          "agent_alpha.yaml",
          "agent_beta.json"
        ]
      },
      {
        "key": "main.log_level",
        "present_in": [
          "agent_gamma.ini"
        ],
        "absent_from": [
          "agent_alpha.yaml",
          "agent_beta.json"
        ]
      }
    ]
  }
}
```
