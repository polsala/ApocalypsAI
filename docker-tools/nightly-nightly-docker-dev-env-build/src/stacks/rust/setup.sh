#!/bin/bash

# Rust stack setup script

set -euo pipefail

log_info() {
    echo "[INFO] $1"
}

log_info "Setting up Rust development environment"

# Create Cargo.toml if it doesn't exist
if [[ ! -f "Cargo.toml" ]]; then
    log_info "Creating Cargo.toml"
    cat > Cargo.toml << 'EOF'
[package]
name = "rust-app"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF
fi

# Create src directory if it doesn't exist
if [[ ! -d "src" ]]; then
    log_info "Creating src directory"
    mkdir -p src
fi

# Create main.rs if it doesn't exist
if [[ ! -f "src/main.rs" ]]; then
    log_info "Creating src/main.rs"
    cat > src/main.rs << 'EOF'
fn main() {
    println!("Hello from your Rust development environment!");
    println!("Rust is awesome!");
}
EOF
fi

# Create .gitignore if it doesn't exist
if [[ ! -f ".gitignore" ]]; then
    log_info "Creating .gitignore"
    cat > .gitignore << 'EOF'
# Rust
/target/
**/*.rs.bk

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

log_info "Rust development environment setup complete!"
