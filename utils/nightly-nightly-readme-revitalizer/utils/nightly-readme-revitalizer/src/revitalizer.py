import re
import sys
import json

def analyze_readme(readme_content: str) -> dict:
    """
    Analyzes README content for common issues and provides revitalization suggestions.
    """
    report = {
        "status": "OK",
        "issues": [],
        "suggestions": []
    }

    # 1. Check for essential sections
    essential_sections = [
        "Installation",
        "Usage",
        "Contributing",
        "License",
        "Features",
        "Examples"
    ]
    
    # Regex to find any level of heading (e.g., # Heading, ## Heading, etc.)
    headings = re.findall(r"^#+\s*(.*?)$", readme_content, re.MULTILINE)

    for section in essential_sections:
        if not any(re.search(r"^" + re.escape(section) + r"$", h, re.IGNORECASE) for h in headings):
            report["issues"].append(f"Missing essential section: '{section}'")
            report["suggestions"].append(f"Consider adding a section titled '{section}' to improve clarity.")
            report["status"] = "NEEDS_REVITALIZATION"

    # 2. Check for placeholder text
    placeholders = [
        "TODO", "FIXME", "YOUR_PROJECT_NAME", "[YOUR_PROJECT_NAME]",
        "[LICENSE_TYPE]", "[AUTHOR_NAME]", "[YEAR]", "[VERSION]",
        "<YOUR_REPO_URL>", "<YOUR_PROJECT_DESCRIPTION>"
    ]
    for placeholder in placeholders:
        if placeholder in readme_content:
            report["issues"].append(f"Found placeholder text: '{placeholder}'")
            report["suggestions"].append(f"Replace '{placeholder}' with actual project information.")
            report["status"] = "NEEDS_REVITALIZATION"

    # 3. Validate internal anchor links
    # Extract all headings and create a set of valid anchor IDs
    # Markdown anchor rules: lowercase, spaces to hyphens, remove special chars
    valid_anchors = set()
    for heading in headings:
        anchor = re.sub(r'[^a-z0-9 -]', '', heading.lower())
        anchor = re.sub(r'\s+', '-', anchor)
        valid_anchors.add(anchor)

    # Find internal links like [text](#anchor)
    internal_links = re.findall(r'\[.*?\]\(#([a-zA-Z0-9_-]+)\)', readme_content)
    for link_anchor in internal_links:
        if link_anchor not in valid_anchors:
            report["issues"].append(f"Broken internal link: '#{link_anchor}' points to a non-existent section.")
            report["suggestions"].append(f"Ensure the section '#{link_anchor}' exists or correct the link.")
            report["status"] = "NEEDS_REVITALIZATION"

    return report

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
        except FileNotFoundError:
            print(json.dumps({"status": "ERROR", "message": f"File not found: {file_path}"}), file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(json.dumps({"status": "ERROR", "message": f"Error reading file: {e}"}), file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin if no file path is provided
        readme_content = sys.stdin.read()

    result = analyze_readme(readme_content)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
