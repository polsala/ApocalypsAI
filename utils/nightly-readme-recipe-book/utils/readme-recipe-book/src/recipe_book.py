import argparse
import sys

def generate_readme(project_name: str, sections: list[str]) -> str:
    """
    Generates a README.md content string based on project name and desired sections.
    """
    readme_parts = []

    # Main Title
    readme_parts.append(f"# {project_name}\n")

    # All possible section content templates
    all_section_templates = {
        "overview": f"## Overview\n\nThis is a brief description of {project_name}. It aims to [purpose] and [key benefit].\n",
        "features": "## Features\n\n*   Feature 1: [Describe feature]\n*   Feature 2: [Describe feature]\n*   Feature 3: [Describe feature]\n\n",
        "installation": "## Installation\n\nTo get started with this project, follow these steps:\n\n```bash\n# Example: Clone the repository\ngit clone https://github.com/your-org/{project_name.lower().replace(' ', '-')}.git\ncd {project_name.lower().replace(' ', '-')}\n\n# Example: Install dependencies (if any)\npip install -r requirements.txt\n```\n\n",
        "usage": "## Usage\n\nHere's how to use {project_name}:\n\n```python\n# Example: Basic usage\n# from your_module import some_function\n# result = some_function('input')\n# print(result)\n```\n\n",
        "configuration": "## Configuration\n\n[Describe any configuration steps or files, e.g., environment variables, config files.]\n\n",
        "api": "## API Reference\n\n[Document your API endpoints, functions, or classes here.]\n\n",
        "contributing": "## Contributing\n\nWe welcome contributions! If you'd like to contribute, please follow these guidelines:\n\n1.  Fork the repository.\n2.  Create a new branch (`git checkout -b feature/your-feature-name`).\n3.  Make your changes.\n4.  Commit your changes (`git commit -m 'Add new feature'`).\n5.  Push to the branch (`git push origin feature/your-feature-name`).\n6.  Open a Pull Request.\n\nPlease ensure your code adheres to the project's coding standards and includes appropriate tests.\n\n",
        "license": "## License\n\nThis project is licensed under the [Your License Name] License - see the [LICENSE](LICENSE) file for details.\n\n",
        "acknowledgements": "## Acknowledgements\n\n*   [Person/Project 1]\n*   [Person/Project 2]\n\n",
        "roadmap": "## Roadmap\n\n*   [ ] Feature A: [Description]\n*   [ ] Feature B: [Description]\n*   [ ] Bug Fix C: [Description]\n\n"
    }

    # Determine which sections to include
    sections_to_process = []
    if not sections: # No sections specified, use a default set
        sections_to_process = [
            "overview", "features", "installation", "usage",
            "contributing", "license"
        ]
    elif "all" in [s.lower() for s in sections]: # 'all' specified, include all known sections
        sections_to_process = list(all_section_templates.keys())
    else: # Specific sections provided
        sections_to_process = [s.lower() for s in sections]

    for section_name in sections_to_process:
        if section_name in all_section_templates:
            readme_parts.append(all_section_templates[section_name].replace('{project_name}', project_name))
        else:
            # Handle unknown sections gracefully by adding a generic placeholder
            readme_parts.append(f"## {section_name.title()}\n\n[Content for {section_name.title()} section]\n\n")

    return "\n".join(readme_parts).strip() + "\n"

def main():
    parser = argparse.ArgumentParser(
        description="Generate a structured README.md template."
    )
    parser.add_argument(
        "--project-name",
        required=True,
        help="The name of your project."
    )
    parser.add_argument(
        "--sections",
        help="Comma-separated list of sections (e.g., 'installation,usage,contributing'). "
             "Available: overview, features, installation, usage, configuration, api, "
             "contributing, license, acknowledgements, roadmap. Use 'all' for all sections."
    )

    args = parser.parse_args()

    if args.sections:
        sections_list = [s.strip() for s in args.sections.split(',') if s.strip()]
    else:
        sections_list = [] # Will trigger default sections in generate_readme

    readme_content = generate_readme(args.project_name, sections_list)
    print(readme_content)

if __name__ == "__main__":
    main()
