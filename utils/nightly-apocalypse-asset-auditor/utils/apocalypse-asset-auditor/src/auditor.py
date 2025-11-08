import os
import json
import argparse

def _read_file_content(filepath):
    """Helper to read file content, returning empty string if file doesn't exist or is unreadable."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except (IOError, OSError):
        return ""

def audit_repo(repo_path):
    """Audits a repository for critical 'survival kit' assets."""
    results = {
        "repo_path": repo_path,
        "status": "healthy",
        "assets": {},
        "issues": []
    }

    critical_files = [
        "README.md",
        "LICENSE",
        "AGENTS.md"
    ]
    critical_dirs = [
        ".github/workflows"
    ]

    # Check critical files
    for filename in critical_files:
        filepath = os.path.join(repo_path, filename)
        exists = os.path.exists(filepath)
        file_info = {"exists": exists, "empty": False, "status": "ok"}

        if exists:
            size = os.path.getsize(filepath)
            file_info["empty"] = (size == 0)
            if size == 0:
                file_info["status"] = "warning"
                results["issues"].append(f"File '{filename}' exists but is empty.")

            if filename == "LICENSE" and not file_info["empty"]:
                content = _read_file_content(filepath)
                # Mock rationale: In a real scenario, this would check for actual license text.
                # For a mock, we check for common placeholder text that indicates an unconfigured license.
                if "Copyright (c) [year] [fullname]" in content or "LICENSE_TEMPLATE" in content:
                    file_info["placeholder"] = True
                    file_info["status"] = "warning"
                    results["issues"].append(f"LICENSE file appears to be a placeholder.")
                else:
                    file_info["placeholder"] = False
        else:
            file_info["status"] = "critical"
            results["issues"].append(f"Critical file '{filename}' is missing.")

        results["assets"][filename] = file_info

    # Check critical directories
    for dirname in critical_dirs:
        dirpath = os.path.join(repo_path, dirname)
        exists = os.path.isdir(dirpath)
        dir_info = {"exists": exists, "empty": False, "status": "ok"}

        if exists:
            # Mock rationale: For this basic auditor, we assume a directory existing implies it's not 'empty' in a critical sense.
            # A more robust check would involve os.listdir and checking if it contains any files.
            pass 
        else:
            dir_info["status"] = "critical"
            results["issues"].append(f"Critical directory '{dirname}' is missing.")

        results["assets"][dirname + '/'] = dir_info # Append '/' for consistency with README example

    if results["issues"]:
        results["status"] = "unhealthy"

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Audit a repository for critical 'survival kit' assets."
    )
    parser.add_argument(
        "--repo-path",
        required=True,
        help="Path to the repository to audit."
    )
    args = parser.parse_args()

    audit_results = audit_repo(args.repo_path)
    print(json.dumps(audit_results, indent=2))
