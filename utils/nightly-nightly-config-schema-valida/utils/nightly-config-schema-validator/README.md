# Schema Shaman's Scrutiny: Nightly Config Schema Validator

## 🧙‍♂️ Description
In the desolate wastes of misconfiguration, the Schema Shaman emerges! This mystical utility ensures your critical configuration files (YAML, JSON) are blessed with structural integrity. By validating them against a predefined schema, it prevents chaotic misconfigurations from wreaking havoc on your systems, bringing order and predictability to your post-apocalyptic deployments.

## ✨ Features
*   **YAML & JSON Support**: Seamlessly validates both YAML and JSON configuration files.
*   **Schema-Driven Validation**: Ensures configurations adhere to a specified structure, data types, and required fields.
*   **Clear Feedback**: Provides detailed error messages upon validation failure, guiding you to the source of the chaos.
*   **Self-Contained**: A standalone Python script with minimal dependencies.

## 🚀 Installation
To invoke the Schema Shaman's powers, you'll need Python 3.8+ and the following incantations:

```bash
pip install pyyaml jsonschema
```

## 🔮 Usage
Run the `validator.py` script from the `src` directory, providing the paths to your configuration file and its corresponding schema.

```bash
python src/validator.py --config <path_to_config_file> --schema <path_to_schema_file>
```

### Example: Validating a YAML Configuration

**`my_app_config.yaml`**:
```yaml
server:
  host: localhost
  port: 8080
database:
  type: postgres
  connection_string: "host=db user=admin password=secret"
features:
  - analytics
  - notifications
```

**`my_app_schema.yaml`**:
```yaml
type: object
properties:
  server:
    type: object
    properties:
      host: { type: string }
      port: { type: integer, minimum: 1024, maximum: 65535 }
    required: [host, port]
  database:
    type: object
    properties:
      type: { type: string, enum: [postgres, mysql, sqlite] }
      connection_string: { type: string }
    required: [type, connection_string]
  features:
    type: array
    items: { type: string }
required: [server, database]
additionalProperties: false
```

**Command**:
```bash
python src/validator.py --config my_app_config.yaml --schema my_app_schema.yaml
```

**Expected Output (Success)**:
```
✅ Configuration 'my_app_config.yaml' is valid according to schema 'my_app_schema.yaml'. The spirits are pleased!
```

### Example: Invalid Configuration

If `my_app_config.yaml` was missing the `port`:

**`my_app_config_invalid.yaml`**:
```yaml
server:
  host: localhost
database:
  type: postgres
  connection_string: "host=db user=admin password=secret"
```

**Command**:
```bash
python src/validator.py --config my_app_config_invalid.yaml --schema my_app_schema.yaml
```

**Expected Output (Failure)**:
```
❌ Configuration 'my_app_config_invalid.yaml' failed validation against schema 'my_app_schema.yaml':
'port' is a required property
```
