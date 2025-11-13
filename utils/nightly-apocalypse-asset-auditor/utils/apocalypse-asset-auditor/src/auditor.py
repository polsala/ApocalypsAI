import os
import sys

def scan_repository(repo_path: str, critical_assets: list[str]) -> dict:
    """
    Scans the specified repository path for the presence of critical assets.
    Returns a dictionary with asset names as keys and their status (True/False) as values.
    For directories like '.github/workflows/', it also checks for .yml files.
    """
    results = {}
    missing_count = 0

    for asset in critical_assets:
        full_path = os.path.join(repo_path, asset)
        if os.path.isdir(full_path):
            # Special handling for directories like .github/workflows/
            if os.path.exists(full_path):
                workflow_files = [f for f in os.listdir(full_path) if f.endswith(('.yml', '.yaml'))]
                if workflow_files:
                    results[asset] = {"present": True, "type": "dir", "count": len(workflow_files)}
                else:
                    results[asset] = {"present": False, "type": "dir", "reason": "No workflow files found"}
                    missing_count += 1
            else:
                results[asset] = {"present": False, "type": "dir", "reason": "Directory not found"}
                missing_count += 1
        else:
            # Regular file check
            if os.path.exists(full_path):
                results[asset] = {"present": True, "type": "file"}
            else:
                results[asset] = {"present": False, "type": "file"}
                missing_count += 1
    
    return {"results": results, "missing_count": missing_count}

def main():
    repo_path = os.getcwd() # Default to current working directory
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]

    # Define the critical assets to check
    CRITICAL_ASSETS = [
        "README.md",
        "LICENSE",
        "CONTRIBUTING.md",
        ".gitignore",
        ".github/workflows/" # This will be checked as a directory
    ]

    print("\n🚨 Apocalypse Asset Auditor Report 🚨\n")
    print(f"Scanning repository at: {repo_path}\n")

    audit_report = scan_repository(repo_path, CRITICAL_ASSETS)
    results = audit_report["results"]
    missing_count = audit_report["missing_count"]

    for asset, status in results.items():
        if status["present"]:
            if status["type"] == "dir":
                print(f"✅ {asset}: Directory exists with {status['count']} workflows. Automation online!")
            else:
                print(f"✅ {asset}: Present and accounted for.")
        else:
            if status["type"] == "dir":
                print(f"❌ {asset}: Missing! {status['reason']}. Consider adding essential automation.")
            else:
                print(f"❌ {asset}: Missing! Consider adding guidelines for new survivors.")

    print("\n---")
    if missing_count == 0:
        print("--- Bunker Readiness Status: FULLY STOCKED ---")
        print("(All critical assets are present. You are ready for anything!)")
        sys.exit(0)
    else:
        print("--- Bunker Readiness Status: PARTIALLY STOCKED ---")
        print(f"({missing_count} critical asset(s) are missing. Recommend immediate action!)")
        sys.exit(1)

if __name__ == "__main__":
    main()
