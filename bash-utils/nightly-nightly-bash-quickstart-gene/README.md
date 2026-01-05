# Nightly Bash Quickstart Generator

A whimsical-yet-useful Bash utility that generates project quickstart guides from template files with customizable placeholders.

## Features

- Generate quickstart guides from template files
- Replace placeholders with user-provided values
- Support for multiple template formats
- Interactive mode for easy customization
- Batch processing for multiple templates

## Usage

### Basic Usage

```bash
# Generate a quickstart guide from a template
./quickstart-generator.sh --template my-template.md --output quickstart.md

# Interactive mode
./quickstart-generator.sh --interactive

# Batch processing
./quickstart-generator.sh --batch templates/ --output-dir guides/
```

### Template Format

Templates use a simple placeholder syntax:

```markdown
# Project Quickstart

## Getting Started

Welcome to {{PROJECT_NAME}}!

To get started, run:

```bash
{{INSTALL_COMMAND}}
{{START_COMMAND}}
```

## Configuration

Set these environment variables:

- `API_KEY={{API_KEY}}`
- `DEBUG={{DEBUG_MODE}}`
```

### Command Line Options

- `--template <file>`: Input template file
- `--output <file>`: Output file (default: quickstart.md)
- `--interactive`: Run in interactive mode
- `--batch <dir>`: Process all templates in directory
- `--output-dir <dir>`: Output directory for batch mode
- `--values <file>`: JSON file with placeholder values
- `--help`: Show help message

## Examples

### Simple Template Generation

```bash
./quickstart-generator.sh --template templates/web-app.md --output docs/quickstart.md
```

### Interactive Mode

```bash
./quickstart-generator.sh --interactive
# Prompts for template file and placeholder values
```

### Batch Processing

```bash
./quickstart-generator.sh --batch templates/ --output-dir guides/ --values config.json
```

## Installation

1. Make the script executable:
   ```bash
   chmod +x quickstart-generator.sh
   ```

2. Run directly or copy to your PATH:
   ```bash
   cp quickstart-generator.sh /usr/local/bin/quickstart-generator
   ```

## Requirements

- Bash 4.0+
- jq (for JSON processing)

## License

MIT
