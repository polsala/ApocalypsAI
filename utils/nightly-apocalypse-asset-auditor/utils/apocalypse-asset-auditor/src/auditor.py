import os
import sys

def audit_repo(repo_path: str, critical_assets: list[str]) -> dict:
    """
    Audits a repository path for the presence of critical files and directories.

    Args:
        repo_path: The absolute or relative path to the repository.
        critical_assets: A list of strings representing critical files or directories.
                         Directories should end with a '/'.

    Returns:
        A dictionary with 'present' and 'missing' lists of assets.
    """
    results = {
        'present': [],
        'missing': []
    }

    if not os.path.isdir(repo_path):
        print(f"Error: Repository path '{repo_path}' does not exist or is not a directory.", file=sys.stderr)
        return results # Return empty results for error case

    for asset in critical_assets:
        full_path = os.path.join(repo_path, asset)
        if asset.endswith('/'): # It's a directory
            if os.path.isdir(full_path):
                results['present'].append(asset)
            else:
                results['missing'].append(asset)
        else: # It's a file
            if os.path.isfile(full_path):
                results['present'].append(asset)
            else:
                results['missing'].append(asset)

    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/auditor.py <repository_path>", file=sys.stderr)
        sys.exit(1)

    repo_path = sys.argv[1]

    # Define the critical assets for the ApocalypsAI project
    # Directories are indicated by a trailing slash.
    critical_assets = [
        "README.md",
        "LICENSE",
        "AGENTS.md",
        ".github/workflows/",
        "agents/",
        "utils/"
    ]

    print(f"Auditing repository: {repo_path}\n")
    print("--- Critical Assets Check ---\n")

    audit_results = audit_repo(repo_path, critical_assets)

    if not audit_results['present'] and not audit_results['missing'] and not os.path.isdir(repo_path):
        sys.exit(1) # Exit with error if repo_path was invalid

    for asset in critical_assets:
        if asset in audit_results['present']:
            print(f"✅  {asset}")
        else:
            print(f"❌  {asset} (Missing)")

    print("\n--- Audit Summary ---\n")
    total_assets = len(critical_assets)
    present_count = len(audit_results['present'])
    missing_count = len(audit_results['missing'])

    print(f"Total Assets Checked: {total_assets}")
    print(f"Present Assets: {present_count}")
    print(f"Missing Assets: {missing_count}")

    if missing_count > 0:
        print("\nMissing Assets List:")
        for asset in audit_results['missing']:
            print(f"- {asset}")
        print("\nRepository is NOT apocalypse-ready. Address the missing assets!")
        sys.exit(1) # Exit with error if assets are missing
    else:
        print("\nRepository is apocalypse-ready! All critical assets are present.")
        sys.exit(0)

if __name__ == "__main__":
    main()
