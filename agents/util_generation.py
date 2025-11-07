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


def parse_payload(raw: str) -> GeneratedUtility:
    json_blob = _extract_json(raw)
    try:
        data = json.loads(json_blob)
    except json.JSONDecodeError as exc:
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

    return GeneratedUtility(name=name, summary=summary, files=generated_files)


def write_utility(util: GeneratedUtility, *, prefix: str | None = None) -> Path:
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
    base = Path("utils")
    if not base.exists():
        return []
    return sorted(
        entry.name for entry in base.iterdir() if entry.is_dir() and not entry.name.startswith(".")
    )


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
