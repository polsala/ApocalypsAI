import os
import re
from typing import List, Dict

class ReadmeRevivalist:
    def __init__(self, readme_path: str):
        self.readme_path = readme_path
        self.content = ""
        if os.path.exists(self.readme_path):
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                self.content = f.read()

    def _check_missing_sections(self) -> List[str]:
        issues = []
        common_sections = ["Installation", "Usage", "Contributing", "License"]
        for section in common_sections:
            # Look for markdown headers like # Section or ## Section
            if not re.search(rf"^[#]+\s*{re.escape(section)}\b", self.content, re.MULTILINE | re.IGNORECASE):
                issues.append(f"Missing or improperly formatted section: '{section}'")
        return issues

    def _check_placeholders(self) -> List[str]:
        issues = []
        placeholders = ["TODO", "FIXME", "YOUR_PROJECT_NAME", "PROJECT_DESCRIPTION"]
        for placeholder in placeholders:
            if re.search(rf"\b{re.escape(placeholder)}\b", self.content, re.IGNORECASE):
                issues.append(f"Found placeholder text: '{placeholder}'")
        return issues

    def _check_link_syntax(self) -> List[str]:
        issues = []
        # Regex to find markdown links: [text](url) or ![alt text](url)
        links = re.findall(r"!?\[.*?\]\((.*?)\)", self.content)
        for link_url in links:
            if not link_url.strip():
                issues.append("Found a link with an empty URL: `[]()` or `![]()`")
            elif " " in link_url.strip(): # Simple check for spaces in URL, often indicates malformed
                issues.append(f"Found a link with spaces in the URL: '{link_url}'")
        return issues

    def revive(self) -> Dict[str, List[str]]:
        if not self.content:
            return {"error": ["README file not found or empty."]}

        report = {
            "missing_sections": self._check_missing_sections(),
            "placeholders": self._check_placeholders(),
            "link_syntax_issues": self._check_link_syntax(),
        }
        return report

def main():
    # This main function is for direct execution and demonstration.
    # It assumes it's run from a directory containing a README.md file.
    readme_file = "README.md"
    if not os.path.exists(readme_file):
        print(f"Error: {readme_file} not found in current directory.")
        print("Please run this utility from a directory containing a README.md file.")
        return

    revivalist = ReadmeRevivalist(readme_file)
    report = revivalist.revive()

    if "error" in report:
        print(f"Error: {report['error'][0]}")
        return

    has_issues = False
    for category, issues in report.items():
        if issues:
            has_issues = True
            print(f"\n--- {category.replace('_', ' ').title()} ---")
            for issue in issues:
                print(f"- {issue}")

    if not has_issues:
        print("\nREADME looks great! No revival needed.")
    else:
        print("\nREADME revival report complete. Consider addressing the issues above.")

if __name__ == "__main__":
    main()
