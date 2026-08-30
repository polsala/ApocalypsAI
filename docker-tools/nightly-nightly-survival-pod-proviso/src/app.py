import argparse
import json
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

def load_manifest(manifest_path):
    """Loads a manifest file (JSON or YAML) and returns its content."""
    _, ext = os.path.splitext(manifest_path)
    with open(manifest_path, 'r') as f:
        if ext.lower() == '.json':
            return json.load(f)
        elif ext.lower() in ('.yml', '.yaml'):
            return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported manifest file type: {ext}")

def render_template(blueprint_path, context):
    """Renders a Jinja2 template with the given context."""
    template_dir = os.path.dirname(blueprint_path)
    template_name = os.path.basename(blueprint_path)

    env = Environment(
        loader=FileSystemLoader(template_dir or './'), # Use current dir if no path given
        autoescape=select_autoescape(['html', 'xml', 'j2', 'yml', 'yaml'])
    )
    template = env.get_template(template_name)
    return template.render(context)

def validate_compose_yaml(compose_content):
    """Performs basic validation on the generated Docker Compose YAML."""
    try:
        parsed_yaml = yaml.safe_load(compose_content)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML syntax in generated compose file: {e}")

    if not isinstance(parsed_yaml, dict):
        raise ValueError("Generated compose file is not a valid YAML dictionary.")

    if 'services' not in parsed_yaml or not isinstance(parsed_yaml['services'], dict):
        raise ValueError("Generated compose file must contain a 'services' section.")

    # Add more specific checks if needed, e.g., for each service
    for service_name, service_config in parsed_yaml['services'].items():
        if not isinstance(service_config, dict):
            raise ValueError(f"Service '{service_name}' configuration is not a dictionary.")
        if 'image' not in service_config:
            print(f"Warning: Service '{service_name}' does not specify an image.")

    return True

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Survival Pod Provisor: Generate and validate Docker Compose files."
    )
    parser.add_argument(
        "--blueprint",
        required=True,
        help="Path to the Jinja2 Docker Compose blueprint file."
    )
    parser.add_argument(
        "--manifest",
        required=True,
        help="Path to the JSON or YAML manifest file containing variables."
    )

    args = parser.parse_args()

    try:
        manifest_data = load_manifest(args.manifest)
        rendered_compose = render_template(args.blueprint, manifest_data)
        validate_compose_yaml(rendered_compose)
        print(rendered_compose)
    except Exception as e:
        print(f"Error provisioning pod: {e}")
        exit(1)

if __name__ == "__main__":
    main()
