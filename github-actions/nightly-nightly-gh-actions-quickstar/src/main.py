import argparse
import os
import sys
import yaml
from datetime import datetime
from typing import Dict, List, Optional


def generate_workflow(
    template: str,
    output: str,
    matrix: Optional[str] = None,
    security: bool = False,
    permissions: Optional[Dict[str, str]] = None,
) -> str:
    """
    Generate a GitHub Actions workflow file based on the specified template.
    
    Args:
        template: The template type (ci, deploy, security, release)
        output: Output file path
        matrix: Matrix strategy configuration (format: "key:val1,val2")
        security: Whether to include security best practices
        permissions: Custom permissions configuration
    
    Returns:
        Generated workflow content as string
    """
    # Base workflow structure
    workflow = {
        "name": f"{template.upper()} Workflow",
        "on": {},
        "jobs": {}
    }
    
    # Set permissions if security mode or custom permissions provided
    if security or permissions:
        workflow["permissions"] = permissions or {
            "contents": "read",
            "security-events": "write",
            "actions": "read"
        }
    
    # Configure triggers based on template
    if template == "ci":
        workflow["on"] = {
            "push": {"branches": ["main", "master"]},
            "pull_request": {"branches": ["main", "master"]}
        }
        
        # CI jobs
        workflow["jobs"] = {
            "test": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {"name": "Checkout code", "uses": "actions/checkout@v4"},
                    {"name": "Setup Python", "uses": "actions/setup-python@v5", "with": {"python-version": "3.11"}},
                    {"name": "Install dependencies", "run": "python -m pip install --upgrade pip && pip install -r requirements.txt"},
                    {"name": "Run tests", "run": "python -m pytest tests/ -v"},
                    {"name": "Security scan", "run": "pip install bandit && bandit -r . -f json -o bandit-report.json", "if": security}
                ]
            }
        }
        
        if matrix:
            workflow["jobs"]["test"]["strategy"] = parse_matrix(matrix)
            
    elif template == "deploy":
        workflow["on"] = {"release": {"types": ["published"]}}
        
        # Deployment jobs with environment-specific steps
        workflow["jobs"] = {
            "deploy-staging": {
                "runs-on": "ubuntu-latest",
                "environment": "staging",
                "steps": [
                    {"name": "Checkout code", "uses": "actions/checkout@v4"},
                    {"name": "Deploy to staging", "run": "echo 'Deploying to staging environment'"}
                ]
            },
            "deploy-production": {
                "runs-on": "ubuntu-latest",
                "needs": ["deploy-staging"],
                "environment": "production",
                "steps": [
                    {"name": "Checkout code", "uses": "actions/checkout@v4"},
                    {"name": "Deploy to production", "run": "echo 'Deploying to production environment'"}
                ]
            }
        }
        
        if matrix:
            workflow["jobs"]["deploy-staging"]["strategy"] = parse_matrix(matrix)
            
    elif template == "security":
        workflow["on"] = {
            "push": {"branches": ["main", "master"]},
            "pull_request": {"branches": ["main", "master"]},
            "schedule": [{"cron": "0 2 * * 1"}]  # Weekly on Monday at 2 AM
        }
        
        # Security-focused jobs
        workflow["jobs"] = {
            "codeql-analysis": {
                "runs-on": "ubuntu-latest",
                "permissions": {"security-events": "write"},
                "steps": [
                    {"name": "Checkout code", "uses": "actions/checkout@v4"},
                    {"name": "Initialize CodeQL", "uses": "github/codeql-action/init@v3", "with": {"languages": "python"}},
                    {"name": "Perform CodeQL Analysis", "uses": "github/codeql-action/analyze@v3"}
                ]
            },
            "dependency-scan": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {"name": "Checkout code", "uses": "actions/checkout@v4"},
                    {"name": "Setup Python", "uses": "actions/setup-python@v5", "with": {"python-version": "3.11"}},
                    {"name": "Install dependencies", "run": "python -m pip install --upgrade pip && pip install safety"},
                    {"name": "Run dependency scan", "run": "safety check --json --output safety-report.json"}
                ]
            }
        }
        
    elif template == "release":
        workflow["on"] = {"push": {"tags": ["v*.*.*"]}}
        
        # Release automation jobs
        workflow["jobs"] = {
            "build": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {"name": "Checkout code", "uses": "actions/checkout@v4"},
                    {"name": "Setup Python", "uses": "actions/setup-python@v5", "with": {"python-version": "3.11"}},
                    {"name": "Build package", "run": "python setup.py sdist bdist_wheel"},
                    {"name": "Upload artifacts", "uses": "actions/upload-artifact@v4", "with": {"name": "dist", "path": "dist/"}}
                ]
            },
            "publish": {
                "runs-on": "ubuntu-latest",
                "needs": ["build"],
                "steps": [
                    {"name": "Download artifacts", "uses": "actions/download-artifact@v4", "with": {"name": "dist", "path": "."}},
                    {"name": "Publish to PyPI", "uses": "pypa/gh-action-pypi-publish@release/v1", "with": {"password": "${{ secrets.PYPI_API_TOKEN }}"}}
                ]
            }
        }
        
        if matrix:
            workflow["jobs"]["build"]["strategy"] = parse_matrix(matrix)
    
    else:
        raise ValueError(f"Unknown template: {template}")
    
    # Convert to YAML string
    workflow_yaml = yaml.dump(workflow, default_flow_style=False, sort_keys=False)
    
    # Ensure proper formatting and add header comment
    header = f"# Generated by Nightly GitHub Actions Quickstart on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Template: {template}
# Security mode: {security}
\n"
    
    return header + workflow_yaml


def parse_matrix(matrix_str: str) -> Dict:
    """
    Parse matrix strategy string into dictionary.
    
    Format: "key:val1,val2" or "key1:val1,val2;key2:val3,val4"
    """
    matrix = {"matrix": {}}
    
    if not matrix_str:
        return matrix
    
    for item in matrix_str.split(";"):
        if ":" not in item:
            continue
        
        key, values = item.split(":", 1)
        matrix["matrix"][key.strip()] = [v.strip() for v in values.split(",")]
    
    return matrix


def save_workflow(content: str, output_path: str) -> None:
    """Save workflow content to file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(content)
    print(f"Workflow generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate GitHub Actions workflow files")
    parser.add_argument("--template", required=True, choices=["ci", "deploy", "security", "release"],
                       help="Workflow template to use")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--matrix", help="Matrix strategy (format: key:val1,val2)")
    parser.add_argument("--security", action="store_true", help="Include security best practices")
    parser.add_argument("--permissions", help="Custom permissions (format: key:val,key2:val2)")
    
    args = parser.parse_args()
    
    try:
        # Parse custom permissions if provided
        permissions = None
        if args.permissions:
            permissions = {}
            for item in args.permissions.split(","):
                if ":" in item:
                    key, val = item.split(":", 1)
                    permissions[key.strip()] = val.strip()
        
        # Generate workflow
        content = generate_workflow(
            template=args.template,
            output=args.output,
            matrix=args.matrix,
            security=args.security,
            permissions=permissions
        )
        
        # Save to file
        save_workflow(content, args.output)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
