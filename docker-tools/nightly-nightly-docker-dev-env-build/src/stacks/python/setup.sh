#!/bin/bash

# Python stack setup script

set -euo pipefail

log_info() {
    echo "[INFO] $1"
}

log_info "Setting up Python development environment"

# Create virtual environment if it doesn't exist
if [[ ! -d ".venv" ]]; then
    log_info "Creating virtual environment"
    python -m venv .venv
fi

# Create default Python files
if [[ ! -f "main.py" ]]; then
    log_info "Creating main.py"
    cat > main.py << 'EOF'
#!/usr/bin/env python3
"""Main entry point for the application."""

import sys


def main():
    """Main function."""
    print("Hello from your Python development environment!")
    print(f"Python version: {sys.version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
EOF
    chmod +x main.py
fi

# Create .gitignore if it doesn't exist
if [[ ! -f ".gitignore" ]]; then
    log_info "Creating .gitignore"
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/
.pytest_cache/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
fi

log_info "Python development environment setup complete!"
