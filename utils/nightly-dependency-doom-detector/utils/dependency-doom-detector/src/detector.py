import sys
import tomli
import re
from typing import List, Dict, Any

# Mock rationale: These lists simulate external knowledge bases or vulnerability databases.
# In a real-world scenario, these would be fetched from a live service or a regularly updated local database.
# For this self-contained utility, they provide deterministic 'doom' criteria.
ANCIENT_CURSE_DEPS = {
    "ancient-lib": "0.5.0", # Example: any version of ancient-lib is considered ancient
    "old-framework": "1.0.0",
}

SHADOWY_VULNERABILITY_DEPS = {
    "vulnerable-dep": ["2.1.0", "2.1.1"], # Example: specific versions of vulnerable-dep have issues
    "risky-package": ["3.0.0"],
}

class DependencyDoomDetector:
    def __init__(self, pyproject_path: str):
        self.pyproject_path = pyproject_path
        self.doomed_dependencies: List[Dict[str, str]] = []
        self.clean_dependencies: List[str] = []

    def _parse_pyproject_toml(self) -> Dict[str, Any]:
        try:
            with open(self.pyproject_path, "rb") as f:
                return tomli.load(f)
        except FileNotFoundError:
            print(f"Error: pyproject.toml not found at {self.pyproject_path}", file=sys.stderr)
            sys.exit(1)
        except tomli.TOMLDecodeError as e:
            print(f"Error parsing pyproject.toml: {e}", file=sys.stderr)
            sys.exit(1)

    def _detect_doom(self, dep_name: str, dep_spec: str):
        # Rule 1: Fragile Foundation (Exact Version Pinning)
        if re.match(r"^[^<>=~]+==[0-9]+\.[0-9]+\.[0-9]+$", dep_spec):
            self.doomed_dependencies.append({
                "dependency": dep_spec,
                "doom_type": "Fragile Foundation",
                "description": "Pinned to an exact version, preventing critical updates and security patches. Consider using `>=` or `~=`."
            })
            return

        # Rule 2: Ancient Curse (Known Ancient Dependency)
        if dep_name in ANCIENT_CURSE_DEPS:
            self.doomed_dependencies.append({
                "dependency": dep_spec,
                "doom_type": "Ancient Curse",
                "description": f"This dependency ('{dep_name}') is known to be extremely old and likely unmaintained. Seek modern alternatives."
            })
            return

        # Rule 3: Shadowy Vulnerability (Known Vulnerable Version)
        if dep_name in SHADOWY_VULNERABILITY_DEPS:
            # Extract version from spec (simplistic for demonstration)
            match = re.search(r"([0-9]+\.[0-9]+\.[0-9]+)", dep_spec)
            if match:
                version = match.group(1)
                if version in SHADOWY_VULNERABILITY_DEPS[dep_name]:
                    self.doomed_dependencies.append({
                        "dependency": dep_spec,
                        "doom_type": "Shadowy Vulnerability",
                        "description": f"A known (mocked) security flaw has been detected in '{dep_name}' version {version}. Immediate action required!"
                    })
                    return
        
        self.clean_dependencies.append(dep_spec)

    def run(self):
        data = self._parse_pyproject_toml()
        dependencies = data.get("project", {}).get("dependencies", [])

        if not dependencies:
            print("No dependencies found in pyproject.toml.")
            return

        for dep_spec in dependencies:
            # Extract package name (simplistic: everything before first non-alphanumeric or operator)
            match = re.match(r"^([a-zA-Z0-9._-]+)", dep_spec)
            dep_name = match.group(1) if match else dep_spec.split(' ')[0].split(';')[0].strip()
            self._detect_doom(dep_name, dep_spec)

        self._generate_report()

    def _generate_report(self):
        report = "# Dependency Doom Report\n\n"

        if self.doomed_dependencies:
            report += "## Detected Doomsayers:\n\n"
            for doom in self.doomed_dependencies:
                report += f"- **{doom['dependency']}**\n"
                report += f"  - **Doom Type**: {doom['doom_type']}\n"
                report += f"  - **Description**: {doom['description']}\n\n"
        else:
            report += "## All Clear!\n\nNo signs of impending doom detected in your dependencies. Keep vigilant!\n\n"

        if self.clean_dependencies:
            report += "## Vigilant Dependencies:\n\n"
            for dep in self.clean_dependencies:
                report += f"- {dep}\n"
            report += "\n"

        print(report)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/detector.py <path_to_pyproject.toml>", file=sys.stderr)
        sys.exit(1)

    detector = DependencyDoomDetector(sys.argv[1])
    detector.run()
