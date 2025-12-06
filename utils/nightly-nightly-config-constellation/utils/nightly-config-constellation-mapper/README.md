# Nightly Config Constellation Mapper

## Overview

The Nightly Config Constellation Mapper is a whimsical yet practical utility designed to help you navigate the sprawling cosmos of your project's configuration files. It scans a specified directory for configuration files (e.g., `.yaml`, `.json`), parses them, and then maps out all unique top-level keys found across these files. For each key, it lists all the files where it appears, providing a 'constellation map' of your configuration landscape.

This tool is invaluable for:
- Identifying common configuration keys used across different services or modules.
- Spotting potential naming inconsistencies or redundancies.
- Gaining a high-level overview of your project's configuration structure.
- Ensuring 'anarchy with discipline' by understanding your config universe.

## Usage

```bash
python src/mapper.py --directory <path_to_your_project> --extension .yaml
```

### Arguments:
- `--directory` (required): The root directory to start scanning for configuration files.
- `--extension` (required): The file extension of the configuration files to map (e.g., `.yaml`, `.json`). Note: `.yaml` will also match `.yml` files.

## Example Output

```
Config Constellation Map for '.yaml' files in './my_project':

- database_host:
  - ./my_project/config/dev.yaml
  - ./my_project/config/prod.yaml
- api_key:
  - ./my_project/config/dev.yaml
- service_port:
  - ./my_project/service_a/config.yaml
  - ./my_project/service_b/config.yaml
- feature_flags:
  - ./my_project/service_a/config.yaml
```

## Development

This utility is written in Python 3.11 and uses `PyYAML` for YAML parsing. It is designed to be self-contained and has deterministic, offline tests.
