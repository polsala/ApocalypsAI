from __future__ import annotations

import json
import re
import secrets
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import List, Any


class PayloadError(RuntimeError):
    """Raised when the LLM response cannot be parsed as a utility payload."""


@dataclass
class GeneratedFile:
    path: str
    content: str


@dataclass
class GeneratedUtility:
    name: str
    summary: str
    files: List[GeneratedFile]
    classifier: str | None = None  # V2: classifier for path organization


def _attempt_json_repair(json_str: str) -> str:
    """
    Attempt to repair common JSON formatting issues in LLM-generated content.
    
    This handles cases where the LLM generates truncated JSON by closing
    any unclosed brackets or braces.
    
    Returns the repaired JSON string.
    """
    # Make a copy to work with
    repaired = json_str
    
    # Look for truncated JSON and try to close it properly
    # Count braces and brackets to see if we need to close the structure
    open_braces = repaired.count('{')
    close_braces = repaired.count('}')
    open_brackets = repaired.count('[')
    close_brackets = repaired.count(']')
    
    # If JSON is truncated, try to close it properly
    if open_brackets > close_brackets:
        repaired += ']' * (open_brackets - close_brackets)
    if open_braces > close_braces:
        repaired += '}' * (open_braces - close_braces)
    
    return repaired


def parse_payload(raw: str) -> GeneratedUtility:
    json_blob = _extract_json(raw)
    
    # Try standard JSON parsing first
    try:
        data = json.loads(json_blob)
    except json.JSONDecodeError as exc:
        # If standard parsing fails, try to repair truncated JSON
        try:
            repaired = _attempt_json_repair(json_blob)
            data = json.loads(repaired)
        except json.JSONDecodeError:
            # If repair also fails, raise the original error
            raise PayloadError(f"Invalid JSON payload: {exc}") from exc
    
    if not isinstance(data, dict):
        raise PayloadError("Payload root must be an object.")

    name = str(data.get("util_name") or "").strip()
    summary = str(data.get("summary") or "").strip()
    files = data.get("files")
    if not name:
        raise PayloadError("Missing util_name.")
    if not files or not isinstance(files, list):
        raise PayloadError("files must be a non-empty list.")

    generated_files: List[GeneratedFile] = []
    seen_paths: set[str] = set()
    for entry in files:
        if not isinstance(entry, dict):
            raise PayloadError("Each file entry must be an object.")
        path = str(entry.get("path") or "").strip()
        content = entry.get("content")
        if not path:
            raise PayloadError("File entry missing path.")
        if content is None:
            raise PayloadError(f"File '{path}' missing content.")
        if not isinstance(content, str):
            raise PayloadError(f"File '{path}' content must be a string.")
        normalized = _validate_relative_path(path)
        if normalized in seen_paths:
            raise PayloadError(f"Duplicate file path: {path}")
        seen_paths.add(normalized)
        generated_files.append(GeneratedFile(path=normalized, content=content))

    if not _has_readme(generated_files):
        raise PayloadError("Utility must include a README.md.")
    if not _has_tests(generated_files):
        raise PayloadError("Utility must include at least one file under tests/.")

    # V2: Extract classifier if provided, or infer from files
    classifier = str(data.get("classifier") or "").strip() or None
    if not classifier:
        classifier = _infer_classifier(generated_files, summary)

    return GeneratedUtility(name=name, summary=summary, files=generated_files, classifier=classifier)


def write_utility(util: GeneratedUtility, *, prefix: str | None = None) -> Path:
    # V2: Use classifier-based path if classifier is provided
    if util.classifier:
        base_dir = Path(util.classifier)
    else:
        # Fallback to old utils/ for backward compatibility
        base_dir = Path("utils")
    
    base_dir.mkdir(parents=True, exist_ok=True)
    slug = _build_slug(util.name, prefix=prefix)
    target = base_dir / slug
    suffix = 2
    while target.exists():
        target = base_dir / f"{slug}-{suffix}"
        suffix += 1
    for file in util.files:
        destination = target / Path(PurePosixPath(file.path))
        destination.parent.mkdir(parents=True, exist_ok=True)
        content = file.content.rstrip("\n") + "\n"
        destination.write_text(content, encoding="utf-8")
    return target


def summarize_payload(raw: str, *, file_limit: int = 5) -> str:
    try:
        data: Any = json.loads(_extract_json(raw))
    except Exception:  # noqa: BLE001
        snippet = raw.strip()
        if len(snippet) > 2000:
            snippet = snippet[:2000] + "\n...[truncated]..."
        return snippet
    lines = []
    util_name = data.get("util_name")
    summary = data.get("summary")
    if util_name:
        lines.append(f"util_name: {util_name}")
    if summary:
        lines.append(f"summary: {summary}")
    files = data.get("files")
    if isinstance(files, list):
        lines.append("files:")
        for entry in files[:file_limit]:
            if isinstance(entry, dict):
                path = entry.get("path", "<missing>")
                desc = entry.get("description", "")
                lines.append(f"  - {path}: {desc}")
        if len(files) > file_limit:
            lines.append(f"  ... (+{len(files) - file_limit} more)")
    preview = "\n".join(lines).strip()
    if not preview:
        return "(payload empty)"
    return preview


def list_existing_utils() -> list[str]:
    """List all existing utilities across V2 classifiers and legacy utils/ directory."""
    utils_list = []
    
    # V2: Check all classifier directories
    classifiers = get_v2_classifiers()
    for classifier in classifiers:
        classifier_path = Path(classifier)
        if classifier_path.exists() and classifier_path.is_dir():
            for entry in classifier_path.iterdir():
                if entry.is_dir() and not entry.name.startswith("."):
                    utils_list.append(f"{classifier}/{entry.name}")
    
    # Legacy: Check old utils/ directory
    legacy_base = Path("utils")
    if legacy_base.exists():
        for entry in legacy_base.iterdir():
            if entry.is_dir() and not entry.name.startswith("."):
                utils_list.append(f"utils/{entry.name}")
    
    return sorted(utils_list)


def _extract_json(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        end_lang = stripped.find("\n")
        if end_lang != -1:
            stripped = stripped[end_lang + 1 :]
        if stripped.endswith("```"):
            stripped = stripped[:-3]
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise PayloadError("Unable to locate JSON object in response.")
    return stripped[start : end + 1]


def _validate_relative_path(path: str) -> str:
    if path.startswith("/"):
        raise PayloadError(f"Absolute paths are not allowed: {path}")
    parts = PurePosixPath(path).parts
    if not parts:
        raise PayloadError("Empty file path detected.")
    if any(part in {"..", ""} for part in parts):
        raise PayloadError(f"Unsafe relative path: {path}")
    return str(PurePosixPath(*parts))


def _build_slug(name: str, *, prefix: str | None = None) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not base:
        base = f"util-{secrets.token_hex(2)}"
    if len(base) > 28:
        base = base[:28].rstrip("-")
    prefix_clean = ""
    if prefix:
        prefix_clean = re.sub(r"[^a-z0-9]+", "-", prefix.lower()).strip("-")
    slug = "-".join(filter(None, [prefix_clean, base]))
    return slug or f"util-{secrets.token_hex(2)}"


def _has_readme(files: list[GeneratedFile]) -> bool:
    return any(PurePosixPath(f.path).name.lower() == "readme.md" for f in files)


def _has_tests(files: list[GeneratedFile]) -> bool:
    for file in files:
        parts = [part.lower() for part in PurePosixPath(file.path).parts]
        if "tests" in parts:
            return True
    return False


def get_v2_classifiers() -> list[str]:
    """Return the list of V2 classifier directories."""
    return [
        "python-utils",
        "rust-utils",
        "bash-utils",
        "react-webpage",
        "github-actions",
        "devops-tools",
        "docker-tools",
        "cli-apps",
        "web-apis",
        "js-utils",
        "data-scripts",
        "test-suite-tools",
        "monitoring-scripts",
        "infra-automation",
        "go-utils",
        "typescript-utils",
        "node-utils",
        "java-utils",
        "cpp-utils",
        "ansible-playbooks",
        "terraform-modules",
        "k8s-resources",
        "ci-cd-pipelines",
        "database-scripts",
        "ml-notebooks",
        "api-clients",
    ]


def _infer_classifier(files: list[GeneratedFile], summary: str) -> str:
    """
    Infer the appropriate V2 classifier based on file extensions and summary.
    Returns a classifier string, defaulting to 'python-utils' if no specific match is found.
    """
    # Analyze file extensions
    extensions = set()
    for file in files:
        path = PurePosixPath(file.path)
        if path.suffix:
            extensions.add(path.suffix.lower())
    
    # Check for specific patterns in filenames and content
    filenames = [PurePosixPath(f.path).name.lower() for f in files]
    full_paths = [f.path.lower() for f in files]
    summary_lower = summary.lower()
    
    # GitHub Actions (check early before shell scripts)
    if any(".github/workflows" in p or ".github\\workflows" in p for p in full_paths) or "github action" in summary_lower:
        return "github-actions"
    
    # Rust projects
    if ".rs" in extensions or "cargo.toml" in filenames:
        return "rust-utils"
    
    # Go projects
    if ".go" in extensions or "go.mod" in filenames:
        return "go-utils"
    
    # JavaScript/TypeScript/Node
    if ".ts" in extensions or "tsconfig.json" in filenames:
        return "typescript-utils"
    if ".jsx" in extensions or ".tsx" in extensions or any("react" in s for s in [summary_lower] + filenames):
        return "react-webpage"
    if ".js" in extensions or "package.json" in filenames:
        # Further distinguish between node-utils and js-utils
        if "package.json" in filenames:
            return "node-utils"
        return "js-utils"
    
    # Shell scripts
    if ".sh" in extensions or ".bash" in extensions:
        return "bash-utils"
    
    # Docker
    if "dockerfile" in filenames or any("docker" in f for f in filenames):
        return "docker-tools"
    
    # Kubernetes
    if any(ext in extensions for ext in [".yaml", ".yml"]) and any("k8s" in s or "kubernetes" in s for s in [summary_lower] + filenames):
        return "k8s-resources"
    
    # Terraform
    if ".tf" in extensions or "main.tf" in filenames:
        return "terraform-modules"
    
    # Ansible
    if any("ansible" in f for f in filenames) or "playbook" in summary_lower:
        return "ansible-playbooks"
    
    # Java
    if ".java" in extensions or "pom.xml" in filenames or "build.gradle" in filenames:
        return "java-utils"
    
    # C++
    if any(ext in extensions for ext in [".cpp", ".cc", ".cxx", ".h", ".hpp"]):
        return "cpp-utils"
    
    # Database scripts
    if any(ext in extensions for ext in [".sql"]) or "database" in summary_lower:
        return "database-scripts"
    
    # Machine Learning / Jupyter
    if ".ipynb" in extensions or any("ml" in s or "machine learning" in s for s in [summary_lower]):
        return "ml-notebooks"
    
    # Web APIs (but not API clients)
    api_keywords = ["api", "rest", "graphql", "endpoint"]
    if any(term in summary_lower for term in api_keywords) and "client" not in summary_lower:
        return "web-apis"
    
    # API Clients
    if "api" in summary_lower and "client" in summary_lower:
        return "api-clients"
    
    # DevOps tools (generic)
    if any(term in summary_lower for term in ["devops", "deployment", "infrastructure"]):
        return "devops-tools"
    
    # Monitoring
    if any(term in summary_lower for term in ["monitor", "metrics", "observability", "logging"]):
        return "monitoring-scripts"
    
    # CI/CD
    if any(term in summary_lower for term in ["ci/cd", "continuous integration", "continuous deployment", "pipeline"]):
        return "ci-cd-pipelines"
    
    # Test tools
    if any(term in summary_lower for term in ["test", "testing", "qa"]) and ".py" not in extensions:
        return "test-suite-tools"
    
    # Data scripts (if mentions data processing)
    if any(term in summary_lower for term in ["data", "etl", "transform", "parse"]):
        return "data-scripts"
    
    # CLI apps (generic CLI tools)
    if any(term in summary_lower for term in ["cli", "command-line", "terminal"]):
        return "cli-apps"
    
    # Python (default for .py files)
    if ".py" in extensions:
        return "python-utils"
    
    # Default: use python-utils as fallback for new utilities
    # This ensures V2 paths are used by default
    return "python-utils"

