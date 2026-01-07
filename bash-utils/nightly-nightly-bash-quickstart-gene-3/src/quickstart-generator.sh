#!/bin/bash

# Nightly Bash Quickstart Generator
# A whimsical-yet-useful utility for generating project quickstart guides

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$SCRIPT_DIR/templates"
OUTPUT_DIR="$(pwd)"

# Default values
PROJECT_TYPE="web"
PROJECT_NAME=""
TEMPLATE_FILE=""
OUTPUT_FILE=""
VERBOSE=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default environment variables
: "${QUICKSTART_AUTHOR:=Nightly Developer}" 
: "${QUICKSTART_EMAIL:=dev@example.com}"
: "${QUICKSTART_LICENSE:=MIT}" 
: "${QUICKSTART_VERSION:=1.0.0}"

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Generate project quickstart guides from templates.

OPTIONS:
    -t, --type TYPE        Project type (web, cli, library, api, mobile)
    -p, --project NAME     Project name
    -f, --template FILE    Custom template file
    -o, --output FILE      Output file (default: quickstart.md)
    -l, --list-templates   List available templates
    -v, --verbose          Verbose output
    -h, --help             Show this help message

ENVIRONMENT VARIABLES:
    QUICKSTART_AUTHOR     Author name (default: Nightly Developer)
    QUICKSTART_EMAIL      Author email (default: dev@example.com)
    QUICKSTART_LICENSE    License type (default: MIT)
    QUICKSTART_VERSION    Project version (default: 1.0.0)

EXAMPLES:
    $0 --type web --project "My Awesome Project"
    $0 --template custom.tpl --project "My Project"
    $0 --list-templates

EOF
}

# Function to list available templates
list_templates() {
    print_info "Available project types and templates:"
    echo
    
    if [[ ! -d "$TEMPLATES_DIR" ]]; then
        print_error "Templates directory not found: $TEMPLATES_DIR"
        return 1
    fi
    
    for template in "$TEMPLATES_DIR"/*.tpl; do
        if [[ -f "$template" ]]; then
            template_name=$(basename "$template" .tpl)
            echo "  - $template_name"
        fi
    done
    echo
    print_info "Use --type to specify a template, or --template for custom files."
}

# Function to create templates directory and files
create_templates() {
    mkdir -p "$TEMPLATES_DIR"
    
    # Web template
    cat > "$TEMPLATES_DIR/web.tpl" << 'EOF'
# Quickstart Guide: {{PROJECT_NAME}}

Welcome to {{PROJECT_NAME}}! 🚀

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd {{PROJECT_NAME}}

# Install dependencies
npm install  # or yarn, pip, etc.

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

## Quick Start

```bash
# Start the development server
npm run dev  # or python app.py, etc.

# Open your browser to http://localhost:3000
```

## Configuration

Edit the `.env` file to configure your application:

```env
# Database settings
DATABASE_URL=postgresql://user:password@localhost:5432/db

# API keys
API_KEY=your-api-key-here

# Other settings
PORT=3000
NODE_ENV=development
```

## Features

- 🌟 Feature 1: Description
- 🔧 Feature 2: Description
- 📊 Feature 3: Description

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the {{LICENSE}} License. See `LICENSE` for more information.

## Contact

{{AUTHOR}} - {{EMAIL}}

Project Link: [https://github.com/username/{{PROJECT_NAME}}](https://github.com/username/{{PROJECT_NAME}})
EOF

    # CLI template
    cat > "$TEMPLATES_DIR/cli.tpl" << 'EOF'
# Quickstart Guide: {{PROJECT_NAME}}

Welcome to {{PROJECT_NAME}}! 🛠️

## Installation

### From Source

```bash
# Clone the repository
git clone <repository-url>
cd {{PROJECT_NAME}}

# Build the project
make build  # or cargo build, go build, etc.

# Install globally
sudo make install  # or cargo install, go install, etc.
```

### From Package Manager

```bash
# Install via package manager
brew install {{PROJECT_NAME}}  # or apt, yum, pip, etc.
```

## Usage

```bash
# Basic usage
{{PROJECT_NAME}} --help

# Common commands
{{PROJECT_NAME}} init
{{PROJECT_NAME}} run
{{PROJECT_NAME}} config
```

## Configuration

Create a configuration file at `~/.{{PROJECT_NAME}}/config.yaml`:

```yaml
# Configuration for {{PROJECT_NAME}}
api_key: your-api-key-here
endpoint: https://api.example.com
verbose: true
```

## Examples

```bash
# Initialize a new project
{{PROJECT_NAME}} init my-project

# Run with custom configuration
{{PROJECT_NAME}} run --config custom.yaml

# List available commands
{{PROJECT_NAME}} list-commands
```

## Features

- 🎯 Command 1: Description
- 📝 Command 2: Description
- 🔍 Command 3: Description

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the {{LICENSE}} License. See `LICENSE` for more information.

## Contact

{{AUTHOR}} - {{EMAIL}}

Project Link: [https://github.com/username/{{PROJECT_NAME}}](https://github.com/username/{{PROJECT_NAME}})
EOF

    # Library template
    cat > "$TEMPLATES_DIR/library.tpl" << 'EOF'
# Quickstart Guide: {{PROJECT_NAME}}

Welcome to {{PROJECT_NAME}}! 📚

## Installation

```bash
# Install via package manager
npm install {{PROJECT_NAME}}  # or pip install, go get, etc.
```

## Quick Start

```javascript
// Import the library
const {{PROJECT_NAME}} = require('{{PROJECT_NAME}}');
// or import {{PROJECT_NAME}} from '{{PROJECT_NAME}}';

// Basic usage
const result = {{PROJECT_NAME}}.someFunction();
console.log(result);
```

## API Reference

### Core Functions

- `{{PROJECT_NAME}}.init()` - Initialize the library
- `{{PROJECT_NAME}}.process(data)` - Process input data
- `{{PROJECT_NAME}}.export()` - Export results

### Configuration

```javascript
// Configure the library
{{PROJECT_NAME}}.configure({
  apiKey: 'your-api-key',
  timeout: 5000,
  retries: 3
});
```

## Examples

```javascript
// Example 1: Basic usage
const data = { input: 'hello world' };
const result = {{PROJECT_NAME}}.process(data);
console.log(result);

// Example 2: Advanced configuration
{{PROJECT_NAME}}.configure({
  mode: 'production',
  logging: true
});

const advancedResult = {{PROJECT_NAME}}.advancedProcess(data);
console.log(advancedResult);
```

## Features

- 🚀 Feature 1: Description
- 🔧 Feature 2: Description
- 📊 Feature 3: Description

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the {{LICENSE}} License. See `LICENSE` for more information.

## Contact

{{AUTHOR}} - {{EMAIL}}

Project Link: [https://github.com/username/{{PROJECT_NAME}}](https://github.com/username/{{PROJECT_NAME}})
EOF

    # API template
    cat > "$TEMPLATES_DIR/api.tpl" << 'EOF'
# Quickstart Guide: {{PROJECT_NAME}}

Welcome to {{PROJECT_NAME}}! 🌐

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd {{PROJECT_NAME}}

# Install dependencies
npm install  # or pip install -r requirements.txt, etc.

# Set up environment
cp .env.example .env
# Configure your environment variables
```

## Quick Start

```bash
# Start the API server
npm run start  # or python app.py, etc.

# The API will be available at http://localhost:3000
```

## API Endpoints

### Authentication

```bash
# Get an access token
POST /api/auth/login
{
  "username": "your-username",
  "password": "your-password"
}
```

### Main Endpoints

- `GET /api/users` - List all users
- `POST /api/users` - Create a new user
- `GET /api/users/:id` - Get user by ID
- `PUT /api/users/:id` - Update user
- `DELETE /api/users/:id` - Delete user

## Configuration

Edit the `.env` file:

```env
# Server settings
PORT=3000
NODE_ENV=development

# Database settings
DATABASE_URL=postgresql://user:password@localhost:5432/db

# Authentication
JWT_SECRET=your-jwt-secret
JWT_EXPIRES_IN=24h

# External APIs
EXTERNAL_API_KEY=your-api-key
```

## Examples

```bash
# Get all users
curl -H "Authorization: Bearer your-token" \
     http://localhost:3000/api/users

# Create a new user
curl -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your-token" \
     -d '{"name": "John Doe", "email": "john@example.com"}' \
     http://localhost:3000/api/users
```

## Features

- 🔐 Authentication & Authorization
- 📊 User Management
- 🔍 Search & Filtering
- 📈 Analytics & Metrics

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the {{LICENSE}} License. See `LICENSE` for more information.

## Contact

{{AUTHOR}} - {{EMAIL}}

Project Link: [https://github.com/username/{{PROJECT_NAME}}](https://github.com/username/{{PROJECT_NAME}})
EOF

    # Mobile template
    cat > "$TEMPLATES_DIR/mobile.tpl" << 'EOF'
# Quickstart Guide: {{PROJECT_NAME}}

Welcome to {{PROJECT_NAME}}! 📱

## Installation

### Prerequisites

- Node.js >= 16.0.0
- React Native CLI
- Xcode (iOS) or Android Studio (Android)

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd {{PROJECT_NAME}}

# Install dependencies
npm install

# Install iOS dependencies (iOS only)
cd ios && pod install && cd ..
```

## Quick Start

```bash
# Start Metro bundler
npm start

# Run on iOS
npm run ios

# Run on Android
npm run android
```

## Configuration

Edit the `config.js` file:

```javascript
// Configuration for {{PROJECT_NAME}}
export default {
  apiUrl: 'https://api.example.com',
  debug: true,
  theme: {
    primaryColor: '#007AFF',
    secondaryColor: '#FFFFFF'
  }
};
```

## Features

- 🎨 Beautiful UI Components
- 🔗 API Integration
- 📱 Cross-platform Support
- 🔒 Secure Authentication

## Development

### Adding Screens

1. Create a new component in `src/screens/`
2. Add it to the navigation in `src/navigation/AppNavigator.js`
3. Update the routes in `src/navigation/routes.js`

### Adding API Endpoints

1. Create API functions in `src/services/api.js`
2. Use them in your components
3. Handle loading and error states

## Testing

```bash
# Run unit tests
npm test

# Run E2E tests
npm run test:e2e
```

## Building for Production

```bash
# iOS build
npm run build:ios

# Android build
npm run build:android
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the {{LICENSE}} License. See `LICENSE` for more information.

## Contact

{{AUTHOR}} - {{EMAIL}}

Project Link: [https://github.com/username/{{PROJECT_NAME}}](https://github.com/username/{{PROJECT_NAME}})
EOF

    print_success "Templates created in $TEMPLATES_DIR"
}

# Function to validate inputs
validate_inputs() {
    if [[ -z "$PROJECT_NAME" ]]; then
        print_error "Project name is required. Use --project or -p option."
        show_usage
        exit 1
    fi
    
    if [[ -n "$TEMPLATE_FILE" ]]; then
        if [[ ! -f "$TEMPLATE_FILE" ]]; then
            print_error "Custom template file not found: $TEMPLATE_FILE"
            exit 1
        fi
    else
        # Check if default template exists
        DEFAULT_TEMPLATE="$TEMPLATES_DIR/${PROJECT_TYPE}.tpl"
        if [[ ! -f "$DEFAULT_TEMPLATE" ]]; then
            print_error "Template not found for project type: $PROJECT_TYPE"
            print_info "Available types: $(ls "$TEMPLATES_DIR"/*.tpl 2>/dev/null | xargs -I {} basename {} .tpl | tr '\n' ' ' | sed 's/ $//')"
            exit 1
        fi
    fi
}

# Function to render template
render_template() {
    local template_file="$1"
    local output_file="$2"
    
    if [[ "$VERBOSE" == true ]]; then
        print_info "Rendering template: $template_file"
        print_info "Output file: $output_file"
    fi
    
    # Read template and replace placeholders
    sed "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" "$template_file" | \
    sed "s/{{AUTHOR}}/$QUICKSTART_AUTHOR/g" | \
    sed "s/{{EMAIL}}/$QUICKSTART_EMAIL/g" | \
    sed "s/{{LICENSE}}/$QUICKSTART_LICENSE/g" | \
    sed "s/{{VERSION}}/$QUICKSTART_VERSION/g" > "$output_file"
    
    print_success "Quickstart guide generated: $output_file"
}

# Function to parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -t|--type)
                PROJECT_TYPE="$2"
                shift 2
                ;;
            -p|--project)
                PROJECT_NAME="$2"
                shift 2
                ;;
            -f|--template)
                TEMPLATE_FILE="$2"
                shift 2
                ;;
            -o|--output)
                OUTPUT_FILE="$2"
                shift 2
                ;;
            -l|--list-templates)
                list_templates
                exit 0
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
}

# Main function
main() {
    # Parse command line arguments
    parse_args "$@"
    
    # Create templates if they don't exist
    if [[ ! -d "$TEMPLATES_DIR" ]] || [[ -z $(ls -A "$TEMPLATES_DIR" 2>/dev/null) ]]; then
        create_templates
    fi
    
    # Validate inputs
    validate_inputs
    
    # Set output file
    if [[ -z "$OUTPUT_FILE" ]]; then
        OUTPUT_FILE="$OUTPUT_DIR/quickstart.md"
    fi
    
    # Determine template file
    if [[ -n "$TEMPLATE_FILE" ]]; then
        TEMPLATE_FILE="$TEMPLATE_FILE"
    else
        TEMPLATE_FILE="$TEMPLATES_DIR/${PROJECT_TYPE}.tpl"
    fi
    
    # Generate the quickstart guide
    render_template "$TEMPLATE_FILE" "$OUTPUT_FILE"
    
    if [[ "$VERBOSE" == true ]]; then
        print_info "Generated with author: $QUICKSTART_AUTHOR"
        print_info "Generated with email: $QUICKSTART_EMAIL"
        print_info "Generated with license: $QUICKSTART_LICENSE"
        print_info "Generated with version: $QUICKSTART_VERSION"
    fi
    
    print_success "Quickstart guide generation complete!"
}

# Run main function with all arguments
main "$@"
