# Nightly Config Quirk Quencher

## 🌌 Quench Those Quantum Quirks! 🌌

The digital realm is rife with subtle anomalies – those "quantum quirks" that arise from malformed configuration files, leading to unpredictable system behavior. The Nightly Config Quirk Quencher is your dedicated sentinel, ensuring your JSON, YAML, and INI files are syntactically sound and structurally stable.

Run this utility nightly to preemptively identify and report any configuration file corruption before it can manifest as a full-blown apocalypse.

## ✨ Features

*   **Syntax Validation**: Checks JSON, YAML, and INI files for correct syntax.
*   **Clear Reporting**: Provides immediate feedback on file validity and detailed error messages if parsing fails.
*   **Self-Contained**: A lightweight Python script with minimal dependencies.

## 🚀 Usage

```bash
python src/quirk_quencher.py --file <path_to_config_file> --type <json|yaml|ini>
```

### Examples:

Validate a JSON file:
```bash
python src/quirk_quencher.py --file my_app_config.json --type json
```

Validate a YAML file:
```bash
python src/quirk_quencher.py --file deployment_settings.yaml --type yaml
```

Validate an INI file:
```bash
python src/quirk_quencher.py --file database.ini --type ini
```

## 🛠️ Development

### Dependencies

*   Python 3.8+
*   `PyYAML` (for YAML validation)

Install dependencies:
```bash
pip install PyYAML
```

### Running Tests

```bash
python -m pytest tests/test_quirk_quencher.py
```
