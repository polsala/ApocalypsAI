"""Tests for util_generation.py V2 classifier functionality."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from agents.util_generation import (
    GeneratedFile,
    GeneratedUtility,
    PayloadError,
    _infer_classifier,
    get_v2_classifiers,
    list_existing_utils,
    parse_payload,
    write_utility,
)


def test_get_v2_classifiers():
    """Test that we get a list of V2 classifiers."""
    classifiers = get_v2_classifiers()
    assert isinstance(classifiers, list)
    assert len(classifiers) > 0
    assert "python-utils" in classifiers
    assert "rust-utils" in classifiers
    assert "bash-utils" in classifiers
    assert "react-webpage" in classifiers


def test_infer_classifier_rust():
    """Test classifier inference for Rust projects."""
    files = [
        GeneratedFile("README.md", "# Test"),
        GeneratedFile("src/main.rs", "fn main() {}"),
        GeneratedFile("tests/test_main.rs", "#[test]\nfn test() {}"),
    ]
    classifier = _infer_classifier(files, "A Rust utility")
    assert classifier == "rust-utils"


def test_infer_classifier_go():
    """Test classifier inference for Go projects."""
    files = [
        GeneratedFile("README.md", "# Test"),
        GeneratedFile("main.go", "package main"),
        GeneratedFile("go.mod", "module test"),
    ]
    classifier = _infer_classifier(files, "A Go service")
    assert classifier == "go-utils"


def test_infer_classifier_bash():
    """Test classifier inference for Bash scripts."""
    files = [
        GeneratedFile("README.md", "# Test"),
        GeneratedFile("script.sh", "#!/bin/bash\necho test"),
        GeneratedFile("tests/test.sh", "#!/bin/bash"),
    ]
    classifier = _infer_classifier(files, "A bash automation script")
    assert classifier == "bash-utils"


def test_infer_classifier_typescript():
    """Test classifier inference for TypeScript projects."""
    files = [
        GeneratedFile("README.md", "# Test"),
        GeneratedFile("src/index.ts", "const x: number = 1;"),
        GeneratedFile("tsconfig.json", "{}"),
    ]
    classifier = _infer_classifier(files, "A TypeScript library")
    assert classifier == "typescript-utils"


def test_infer_classifier_react():
    """Test classifier inference for React projects."""
    files = [
        GeneratedFile("README.md", "# Test"),
        GeneratedFile("src/App.jsx", "export default function App() {}"),
        GeneratedFile("package.json", "{}"),
    ]
    classifier = _infer_classifier(files, "A React dashboard")
    assert classifier == "react-webpage"


def test_infer_classifier_docker():
    """Test classifier inference for Docker projects."""
    files = [
        GeneratedFile("README.md", "# Test"),
        GeneratedFile("Dockerfile", "FROM ubuntu"),
        GeneratedFile("tests/test.py", ""),
    ]
    classifier = _infer_classifier(files, "A Docker container")
    assert classifier == "docker-tools"


def test_infer_classifier_terraform():
    """Test classifier inference for Terraform modules."""
    files = [
        GeneratedFile("README.md", "# Test"),
        GeneratedFile("main.tf", "resource"),
        GeneratedFile("tests/test.py", ""),
    ]
    classifier = _infer_classifier(files, "Infrastructure as code")
    assert classifier == "terraform-modules"


def test_infer_classifier_python_default():
    """Test classifier inference defaults to python-utils for Python files."""
    files = [
        GeneratedFile("README.md", "# Test"),
        GeneratedFile("src/main.py", "print('hello')"),
        GeneratedFile("tests/test_main.py", "def test(): pass"),
    ]
    classifier = _infer_classifier(files, "A Python utility")
    assert classifier == "python-utils"


def test_infer_classifier_api():
    """Test classifier inference for API projects."""
    files = [
        GeneratedFile("README.md", "# Test"),
        GeneratedFile("src/api.py", ""),
        GeneratedFile("tests/test.py", ""),
    ]
    classifier = _infer_classifier(files, "A REST API service")
    assert classifier == "web-apis"


def test_parse_payload_with_classifier():
    """Test parsing a payload with explicit classifier."""
    payload_json = {
        "util_name": "test-util",
        "summary": "A test utility",
        "classifier": "rust-utils",
        "files": [
            {"path": "README.md", "content": "# Test"},
            {"path": "tests/test.rs", "content": "#[test]\nfn test() {}"},
        ],
    }
    raw = json.dumps(payload_json)
    util = parse_payload(raw)
    
    assert util.name == "test-util"
    assert util.summary == "A test utility"
    assert util.classifier == "rust-utils"
    assert len(util.files) == 2


def test_parse_payload_without_classifier():
    """Test parsing a payload without explicit classifier (should infer)."""
    payload_json = {
        "util_name": "test-util",
        "summary": "A test utility",
        "files": [
            {"path": "README.md", "content": "# Test"},
            {"path": "src/main.rs", "content": "fn main() {}"},
            {"path": "tests/test.rs", "content": "#[test]\nfn test() {}"},
        ],
    }
    raw = json.dumps(payload_json)
    util = parse_payload(raw)
    
    assert util.name == "test-util"
    assert util.summary == "A test utility"
    assert util.classifier == "rust-utils"  # Should be inferred


def test_write_utility_with_v2_classifier(tmp_path):
    """Test writing a utility to V2 classifier path."""
    # Change to temp directory
    import os
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    
    try:
        util = GeneratedUtility(
            name="test-tool",
            summary="A test tool",
            classifier="rust-utils",
            files=[
                GeneratedFile("README.md", "# Test Tool"),
                GeneratedFile("src/main.rs", "fn main() {}"),
                GeneratedFile("tests/test.rs", "#[test]\nfn test() {}"),
            ],
        )
        
        target = write_utility(util)
        
        # Should be created under rust-utils/
        assert target.parent.name == "rust-utils"
        assert target.exists()
        assert (target / "README.md").exists()
        assert (target / "src" / "main.rs").exists()
        assert (target / "tests" / "test.rs").exists()
    finally:
        os.chdir(original_dir)


def test_write_utility_without_classifier_legacy(tmp_path):
    """Test writing a utility without classifier falls back to utils/ for backward compat."""
    import os
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    
    try:
        util = GeneratedUtility(
            name="test-tool",
            summary="A test tool",
            classifier=None,
            files=[
                GeneratedFile("README.md", "# Test Tool"),
                GeneratedFile("src/main.py", "print('test')"),
                GeneratedFile("tests/test.py", "def test(): pass"),
            ],
        )
        
        target = write_utility(util)
        
        # Should be created under utils/ when classifier is None
        assert target.parent.name == "utils"
        assert target.exists()
    finally:
        os.chdir(original_dir)


def test_list_existing_utils_v2(tmp_path):
    """Test listing utilities across V2 classifiers."""
    import os
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    
    try:
        # Create some V2 utilities
        (tmp_path / "rust-utils" / "tool-1").mkdir(parents=True)
        (tmp_path / "python-utils" / "tool-2").mkdir(parents=True)
        (tmp_path / "bash-utils" / "tool-3").mkdir(parents=True)
        # Create legacy utility
        (tmp_path / "utils" / "legacy-tool").mkdir(parents=True)
        
        utils = list_existing_utils()
        
        assert "rust-utils/tool-1" in utils
        assert "python-utils/tool-2" in utils
        assert "bash-utils/tool-3" in utils
        assert "utils/legacy-tool" in utils
        assert len(utils) == 4
    finally:
        os.chdir(original_dir)


def test_infer_classifier_github_actions():
    """Test classifier inference for GitHub Actions."""
    files = [
        GeneratedFile("README.md", "# Test"),
        GeneratedFile(".github/workflows/test.yml", "name: test"),
        GeneratedFile("tests/test.sh", "#!/bin/bash"),
    ]
    classifier = _infer_classifier(files, "A GitHub Action workflow")
    assert classifier == "github-actions"


def test_infer_classifier_database():
    """Test classifier inference for database scripts."""
    files = [
        GeneratedFile("README.md", "# Test"),
        GeneratedFile("migration.sql", "CREATE TABLE test;"),
        GeneratedFile("tests/test.py", ""),
    ]
    classifier = _infer_classifier(files, "Database migration script")
    assert classifier == "database-scripts"


def test_infer_classifier_monitoring():
    """Test classifier inference for monitoring scripts."""
    files = [
        GeneratedFile("README.md", "# Test"),
        GeneratedFile("monitor.py", ""),
        GeneratedFile("tests/test.py", ""),
    ]
    classifier = _infer_classifier(files, "A monitoring and metrics tool")
    assert classifier == "monitoring-scripts"
