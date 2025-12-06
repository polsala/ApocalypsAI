import os
import argparse

def check_repo_health(repo_path: str) -> list[dict]:
    """
    Scans the specified repository path for common 'ailments' and suggests 'potions'.
    """
    ailments = []

    # Define common files and their corresponding ailments/potions
    checks = [
        {
            "file": "README.md",
            "ailment": "Missing Readme of Lore",
            "description": "README.md not found",
            "potion": "Scroll of Introduction",
            "action": "Create a README.md file to introduce your project."
        },
        {
            "file": "LICENSE",
            "ailment": "Absence of Legal Charm",
            "description": "LICENSE not found",
            "potion": "Tincture of Openness",
            "action": "Add a LICENSE file to define your project's legal terms. Consider MIT or Apache-2.0."
        },
        {
            "file": ".gitignore",
            "ailment": "Unfiltered Artifacts",
            "description": ".gitignore not found",
            "potion": "Elixir of Cleanliness",
            "action": "Create a .gitignore file to prevent unwanted files from being committed."
        },
        {
            "file": "CHANGELOG.md",
            "ailment": "Forgotten Changelog",
            "description": "CHANGELOG.md not found",
            "potion": "Chronicle of Progress",
            "action": "Create a CHANGELOG.md to document all notable changes."
        }
    ]

    for check in checks:
        file_path = os.path.join(repo_path, check["file"])
        if not os.path.exists(file_path):
            ailments.append({
                "ailment": check["ailment"],
                "description": check["description"],
                "potion": check["potion"],
                "action": check["action"]
            })

    # Special check for CONTRIBUTING.md placeholder content
    contributing_file = os.path.join(repo_path, "CONTRIBUTING.md")
    if os.path.exists(contributing_file):
        try:
            with open(contributing_file, 'r', encoding='utf-8') as f:
                content = f.read().strip().lower()
                placeholder_keywords = ["todo", "tbd", "empty", "add content", "work in progress"]
                if not content or any(keyword in content for keyword in placeholder_keywords):
                    ailments.append({
                        "ailment": "Silent Contribution Scroll",
                        "description": "CONTRIBUTING.md exists but is a placeholder",
                        "potion": "Philter of Collaboration",
                        "action": "Flesh out CONTRIBUTING.md with guidelines for contributors."
                    })
        except Exception: # Catch potential encoding errors or permission issues
            pass # Treat as if it's not a placeholder if we can't read it reliably

    return ailments

def main():
    parser = argparse.ArgumentParser(
        description="Scan your repository for common 'ailments' and suggest 'potions'."
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Path to the repository to scan (default: current directory)."
    )
    args = parser.parse_args()

    print("Brewing health potions for your repository...\n")

    detected_ailments = check_repo_health(args.path)

    if detected_ailments:
        print("Detected Ailments and Suggested Potions:\n")
        for ailment in detected_ailments:
            print(f"- Ailment: {ailment['ailment']} ({ailment['description']})")
            print(f"  Potion: {ailment['potion']} (Action: {ailment['action']})\n")
        print("Your repository needs some magical attention!")
    else:
        print("✨ Your repository is in peak magical health! No potions needed.\n")

if __name__ == "__main__":
    main()
