# Nightly Configuration Calibrator

## ⚙️ Calibrate Your Doomsday Devices! ⚙️

The Nightly Configuration Calibrator is a whimsical-yet-essential utility designed to ensure your critical configuration files are always perfectly tuned. It checks a target configuration file against a template of required keys, reporting any missing parameters that could lead to catastrophic (or just annoying) failures.

No more "oops, forgot that environment variable!" moments before the apocalypse.

## Usage

```bash
python src/calibrator.py --config <path_to_your_config_file> --template <path_to_your_template_file>
```

### Arguments:
*   `--config` (or `-c`): Path to the configuration file you want to calibrate (e.g., `.env`, `settings.txt`).
*   `--template` (or `-t`): Path to the template file containing a list of required keys, one per line.

### Configuration File Format:
The utility expects simple key-value pairs, typically one per line, separated by an equals sign (`=`). Lines starting with `#` are treated as comments and ignored.
Example:
```
API_KEY=your_secret_key
DATABASE_URL=postgres://user:pass@host:port/db
DEBUG=True
```

### Template File Format:
A plain text file where each line specifies a required configuration key. Lines starting with `#` are treated as comments and ignored.
Example:
```
API_KEY
DATABASE_URL
LOG_LEVEL
```

## Examples

### Successful Calibration

```bash
# Given config.env:
# API_KEY=abc
# DATABASE_URL=xyz
# LOG_LEVEL=INFO

# Given template.txt:
# API_KEY
# DATABASE_URL

python src/calibrator.py -c config.env -t template.txt
# Output: Configuration calibrated successfully. All required keys are present.
```

### Missing Keys Detected

```bash
# Given config.env:
# API_KEY=abc
# DATABASE_URL=xyz

# Given template.txt:
# API_KEY
# DATABASE_URL
# LOG_LEVEL

python src/calibrator.py -c config.env -t template.txt
# Output: Missing required keys: ['LOG_LEVEL']
#         Configuration requires calibration!
```
