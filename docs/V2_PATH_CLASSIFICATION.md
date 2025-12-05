# V2 Path Classification System

## Overview

The V2 path classification system organizes utilities by their primary language, framework, or technology category. This replaces the old flat `utils/` directory structure with classifier-based subdirectories that make it easier to discover, navigate, and maintain utilities.

## Benefits

- **Better Organization**: Utilities are grouped by technology/purpose
- **Easier Discovery**: Find tools by browsing relevant categories
- **Diversity Encouragement**: Agents are prompted to use varied technologies
- **Scalability**: Clear structure as the utility collection grows
- **Backward Compatibility**: Legacy `utils/` path still works

## Available Classifiers

The system supports 25+ classifiers covering various languages, frameworks, and use cases:

### Language-Specific
- **python-utils** — Python scripts, modules, and utilities
- **rust-utils** — Rust applications, CLI tools, and libraries
- **go-utils** — Go programs and services
- **bash-utils** — Shell scripts and bash utilities
- **js-utils** — JavaScript utilities (browser/generic)
- **node-utils** — Node.js applications and tools
- **typescript-utils** — TypeScript libraries and utilities
- **java-utils** — Java applications and utilities
- **cpp-utils** — C++ programs and libraries

### Framework/Platform-Specific
- **react-webpage** — React web applications and components
- **github-actions** — GitHub Actions workflows and reusable actions
- **docker-tools** — Docker containers, compose files, and utilities
- **ansible-playbooks** — Ansible playbooks and roles
- **terraform-modules** — Terraform modules and configurations
- **k8s-resources** — Kubernetes manifests and resources

### Purpose-Specific
- **cli-apps** — Generic command-line applications (multi-language)
- **web-apis** — Web API services and endpoints
- **api-clients** — API client libraries and wrappers
- **data-scripts** — Data processing, ETL, and transformation scripts
- **database-scripts** — Database migrations, queries, and utilities
- **test-suite-tools** — Testing frameworks and utilities
- **monitoring-scripts** — Monitoring, metrics, and observability tools
- **ci-cd-pipelines** — CI/CD pipeline definitions
- **devops-tools** — General DevOps utilities and scripts
- **infra-automation** — Infrastructure automation scripts
- **ml-notebooks** — Machine learning notebooks and experiments

## How It Works

### 1. Classifier Specification (Explicit)

When generating a utility, the LLM can specify the classifier in the JSON payload:

```json
{
  "util_name": "http-benchmark",
  "summary": "HTTP benchmarking tool",
  "classifier": "rust-utils",
  "files": [
    {"path": "README.md", "content": "..."},
    {"path": "src/main.rs", "content": "..."},
    {"path": "tests/test.rs", "content": "..."}
  ]
}
```

The utility will be created at: `rust-utils/http-benchmark/`

### 2. Classifier Inference (Automatic)

If no classifier is specified, the system automatically infers it from:
- File extensions (`.rs`, `.go`, `.sh`, `.ts`, `.jsx`, etc.)
- Special filenames (`Cargo.toml`, `go.mod`, `package.json`, `Dockerfile`, etc.)
- Summary content (keywords like "API", "monitoring", "database", etc.)

#### Example: Rust Utility
```json
{
  "util_name": "file-hasher",
  "summary": "Fast file hashing utility",
  "files": [
    {"path": "README.md", "content": "..."},
    {"path": "src/main.rs", "content": "..."},
    {"path": "Cargo.toml", "content": "..."},
    {"path": "tests/test.rs", "content": "..."}
  ]
}
```
→ Inferred classifier: `rust-utils`  
→ Created at: `rust-utils/file-hasher/`

#### Example: React Web App
```json
{
  "util_name": "task-dashboard",
  "summary": "Interactive task management dashboard",
  "files": [
    {"path": "README.md", "content": "..."},
    {"path": "src/App.jsx", "content": "..."},
    {"path": "package.json", "content": "..."},
    {"path": "tests/App.test.jsx", "content": "..."}
  ]
}
```
→ Inferred classifier: `react-webpage`  
→ Created at: `react-webpage/task-dashboard/`

#### Example: Bash Script
```json
{
  "util_name": "log-rotator",
  "summary": "Automated log rotation script",
  "files": [
    {"path": "README.md", "content": "..."},
    {"path": "rotate.sh", "content": "#!/bin/bash\n..."},
    {"path": "tests/test.sh", "content": "..."}
  ]
}
```
→ Inferred classifier: `bash-utils`  
→ Created at: `bash-utils/log-rotator/`

### 3. Backward Compatibility

If a classifier is explicitly set to `null` or cannot be inferred, the utility falls back to the legacy `utils/` path:

```python
util = GeneratedUtility(
    name="legacy-tool",
    summary="...",
    classifier=None,  # or omit classifier entirely with no inferrable files
    files=[...]
)
```
→ Created at: `utils/legacy-tool/`

## Inference Logic Priority

The classifier inference follows this priority order:

1. **Explicit classifier field** in JSON → use as-is
2. **GitHub Actions** (.github/workflows/ paths) → `github-actions`
3. **Rust** (.rs files, Cargo.toml) → `rust-utils`
4. **Go** (.go files, go.mod) → `go-utils`
5. **TypeScript** (.ts files, tsconfig.json) → `typescript-utils`
6. **React** (.jsx/.tsx files, "react" in summary) → `react-webpage`
7. **Node.js** (package.json) → `node-utils`
8. **JavaScript** (.js files) → `js-utils`
9. **Bash** (.sh/.bash files) → `bash-utils`
10. **Docker** (Dockerfile) → `docker-tools`
11. **Kubernetes** (.yaml/.yml with k8s keywords) → `k8s-resources`
12. **Terraform** (.tf files) → `terraform-modules`
13. **Ansible** (ansible in filenames, "playbook" in summary) → `ansible-playbooks`
14. **Java** (.java, pom.xml, build.gradle) → `java-utils`
15. **C++** (.cpp/.hpp files) → `cpp-utils`
16. **Database** (.sql files, "database" in summary) → `database-scripts`
17. **ML** (.ipynb, "ml"/"machine learning" in summary) → `ml-notebooks`
18. **Web API** ("api"/"rest"/"graphql" in summary, not "client") → `web-apis`
19. **API Client** ("api" + "client" in summary) → `api-clients`
20. **DevOps** ("devops"/"deployment"/"infrastructure") → `devops-tools`
21. **Monitoring** ("monitor"/"metrics"/"observability") → `monitoring-scripts`
22. **CI/CD** ("ci/cd"/"pipeline") → `ci-cd-pipelines`
23. **Testing** ("test"/"testing"/"qa", non-Python) → `test-suite-tools`
24. **Data Scripts** ("data"/"etl"/"transform") → `data-scripts`
25. **CLI Apps** ("cli"/"command-line") → `cli-apps`
26. **Python** (.py files) → `python-utils`
27. **Default** (if no match) → `python-utils`

## Agent Prompt Enhancements

### Builder Agent
The builder agent's prompt now:
- Lists all available classifiers with examples
- Explicitly encourages choosing the BEST language/tech for the task
- Shows diverse technology options (Rust, Go, Bash, React, TypeScript, etc.)
- Warns against defaulting to Python

Example prompt excerpt:
```
=== LANGUAGE & TECHNOLOGY DIVERSITY ===
STRONGLY ENCOURAGED to use diverse languages and technologies:
- Rust for performance-critical tools, system utilities, CLI apps
- Go for network services, APIs, distributed tools
- Bash for shell scripting, automation, system administration
- JavaScript/TypeScript/Node for web tools, APIs, cross-platform utilities
- React for web interfaces, dashboards, visualization tools
...
```

### Integrator Agent
The integrator agent now:
- Rotates through different technology suggestions daily
- Explicitly challenges itself to use varied languages
- Shows the last 50 utilities to avoid duplication
- Includes a daily "technology suggestion" to encourage creativity

Example prompt excerpt:
```
=== TECHNOLOGY DIVERSITY CHALLENGE ===
TODAY'S SUGGESTION: Try building a concurrent service using Go (classifier: go-utils)!

Other great options to explore:
- Rust for blazing-fast CLI tools and system utilities
- Go for concurrent services and network tools
...
```

## Listing Utilities

The `list_existing_utils()` function now searches across all V2 classifiers:

```python
from agents.util_generation import list_existing_utils

utils = list_existing_utils()
# Returns:
# [
#   'bash-utils/log-rotator',
#   'python-utils/csv-parser',
#   'react-webpage/task-dashboard',
#   'rust-utils/file-hasher',
#   'utils/legacy-tool',
#   ...
# ]
```

## Migration Guide

### For LLMs Generating Utilities

**Old way (still works):**
```json
{
  "util_name": "my-tool",
  "summary": "...",
  "files": [...]
}
```
→ Goes to `utils/my-tool/` (legacy path)

**New way (recommended):**
```json
{
  "util_name": "my-tool",
  "summary": "...",
  "classifier": "rust-utils",
  "files": [...]
}
```
→ Goes to `rust-utils/my-tool/` (V2 path)

**Or let it infer:**
```json
{
  "util_name": "my-tool",
  "summary": "A Rust CLI tool",
  "files": [
    {"path": "src/main.rs", "content": "..."},
    {"path": "Cargo.toml", "content": "..."},
    ...
  ]
}
```
→ Infers `rust-utils` from files → `rust-utils/my-tool/`

### For Developers

No changes needed! The `write_utility()` function automatically handles both V2 and legacy paths:

```python
from agents.util_generation import GeneratedUtility, write_utility

# V2 classifier path
util = GeneratedUtility(
    name="http-bench",
    summary="HTTP benchmarking tool",
    classifier="rust-utils",
    files=[...]
)
path = write_utility(util)
# → rust-utils/http-bench/

# Legacy path (backward compatible)
util = GeneratedUtility(
    name="old-tool",
    summary="...",
    classifier=None,
    files=[...]
)
path = write_utility(util)
# → utils/old-tool/
```

## Examples by Classifier

### Python Utility
```bash
python-utils/
  csv-to-json/
    README.md
    src/converter.py
    tests/test_converter.py
```

### Rust CLI Tool
```bash
rust-utils/
  file-hasher/
    README.md
    Cargo.toml
    src/main.rs
    tests/test.rs
```

### React Web App
```bash
react-webpage/
  task-dashboard/
    README.md
    package.json
    src/
      App.jsx
      components/
    tests/
      App.test.jsx
```

### Bash Automation
```bash
bash-utils/
  log-rotator/
    README.md
    rotate.sh
    tests/test_rotate.sh
```

### Docker Tool
```bash
docker-tools/
  dev-env/
    README.md
    Dockerfile
    docker-compose.yml
    tests/test.sh
```

### GitHub Action
```bash
github-actions/
  auto-label/
    README.md
    action.yml
    .github/
      workflows/
        test.yml
    tests/
      test_action.sh
```

## Testing

Comprehensive tests ensure the V2 system works correctly:

```bash
# Run V2 classification tests
pytest agents/test_util_generation.py -v

# Tests cover:
# - Classifier inference for 10+ languages/frameworks
# - Path creation with V2 classifiers
# - Backward compatibility with legacy paths
# - Listing utilities across all classifiers
```

## Future Enhancements

Potential additions to the classifier system:
- Language-specific variant paths (e.g., `python-utils/ml/`, `python-utils/web/`)
- Dynamic classifier registration
- Custom classifier definitions per repository
- Classifier-specific README templates
- Auto-generated classifier documentation pages
