# Nightly Bash Quickstart Generator

A whimsical-yet-useful Bash utility that generates project quickstart guides from template files with customizable placeholders.

## Features

- Generate quickstart guides from template files
- Replace placeholders with custom values
- Support for multiple template formats
- Interactive mode for easy customization
- Batch processing for multiple templates

## Usage

### Basic Usage

```bash
# Generate a quickstart guide from a template
./src/quickstart-generator.sh --template templates/project-template.md --output docs/QUICKSTART.md

# Interactive mode
./src/quickstart-generator.sh --interactive

# Batch processing
./src/quickstart-generator.sh --batch --templates-dir templates/ --output-dir docs/
```

### Template Format

Templates use a simple placeholder syntax:

```markdown
# {{PROJECT_NAME}} Quickstart Guide

Welcome to {{PROJECT_NAME}}! This guide will help you get started quickly.

## Prerequisites

- {{PREREQUISITE_1}}
- {{PREREQUISITE_2}}

## Installation

```bash
{{INSTALL_COMMAND}}
```

## Usage

```bash
{{USAGE_EXAMPLE}}
```

## Support

For support, contact {{SUPPORT_EMAIL}}.
```

### Configuration File

Create a `config.json` file to define default values:

```json
{
  "PROJECT_NAME": "My Awesome Project",
  "PREREQUISITE_1": "Node.js 16+",
  "PREREQUISITE_2": "npm 8+",
  "INSTALL_COMMAND": "npm install",
  "USAGE_EXAMPLE": "npm start",
  "SUPPORT_EMAIL": "support@example.com"
}
```

## Installation

1. Clone or download this utility
2. Make the script executable: `chmod +x src/quickstart-generator.sh`
3. Run with your templates!

## Examples

### Generate a Python Project Quickstart

```bash
./src/quickstart-generator.sh \
  --template templates/python-template.md \
  --output docs/python-quickstart.md \
  --values "PROJECT_NAME=My Python App" \
  "INSTALL_COMMAND=pip install -r requirements.txt" \
  "USAGE_EXAMPLE=python main.py"
```

### Generate a React Project Quickstart

```bash
./src/quickstart-generator.sh \
  --template templates/react-template.md \
  --output docs/react-quickstart.md \
  --values "PROJECT_NAME=My React App" \
  "INSTALL_COMMAND=npm install" \
  "USAGE_EXAMPLE=npm run dev"
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Submit a pull request

## Support

For issues and questions, please open an issue in the repository.
