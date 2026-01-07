# Nightly Bash Quickstart Generator

A whimsical-yet-useful Bash script that generates project quickstart guides from template files.

## Features

- Generate quickstart guides from customizable templates
- Support for multiple project types (web, CLI, library, etc.)
- Whimsical placeholder text and emojis
- Easy customization with environment variables
- Self-contained with no external dependencies

## Usage

```bash
# Generate a quickstart guide for a web project
./quickstart-generator.sh --type web --project "My Awesome Project"

# Generate with custom template
./quickstart-generator.sh --template custom.tpl --project "My Project"

# List available templates
./quickstart-generator.sh --list-templates
```

## Templates

Available project types:
- `web` - Web application quickstart
- `cli` - Command-line tool quickstart
- `library` - Library/SDK quickstart
- `api` - REST API quickstart
- `mobile` - Mobile app quickstart

## Installation

```bash
chmod +x quickstart-generator.sh
```

## Customization

Set environment variables to customize output:
- `QUICKSTART_AUTHOR` - Your name
- `QUICKSTART_EMAIL` - Your email
- `QUICKSTART_LICENSE` - License type
- `QUICKSTART_VERSION` - Project version

## Examples

```bash
# Generate a web project guide
./quickstart-generator.sh --type web --project "E-commerce Site"

# Generate with custom author
QUICKSTART_AUTHOR="Jane Doe" ./quickstart-generator.sh --type cli --project "Task Manager"
```

## License

MIT - because documentation should be free and fun!
