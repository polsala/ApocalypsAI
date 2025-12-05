"""Tests for the agent PR path conflict detection logic."""
from __future__ import annotations

from unittest.mock import patch
import pytest

from agents import agent_utils


def test_agent_pr_path_validation_logic():
    """Test the path validation logic used in the workflow."""
    
    # Test case 1: Valid agent PR with changes in single utils directory
    with patch("agents.agent_utils.get_pr") as mock_get_pr, \
         patch("agents.agent_utils.get_pr_files") as mock_get_files:
        
        mock_get_pr.return_value = {
            "head": {"ref": "ai/groq-20241205-1234"},
            "state": "open"
        }
        
        mock_get_files.return_value = [
            {"filename": "utils/my-tool/README.md"},
            {"filename": "utils/my-tool/src/main.py"},
            {"filename": "utils/my-tool/tests/test_main.py"}
        ]
        
        pr = agent_utils.get_pr("owner/repo", 1)
        files = agent_utils.get_pr_files("owner/repo", 1)
        
        # Check if it's an agent PR
        branch = pr.get("head", {}).get("ref", "")
        is_ai_pr = any(branch.startswith(f"ai/{agent}-") for agent in ["gemini", "groq", "openrouter"])
        assert is_ai_pr is True
        
        # Validate paths
        changed_files = [f.get("filename", "") for f in files]
        util_dirs = set()
        violations = []
        
        for filepath in changed_files:
            if not filepath.startswith("utils/"):
                violations.append(f"File outside utils/: {filepath}")
            else:
                parts = filepath.split("/")
                if len(parts) >= 2:
                    util_name = parts[1]
                    util_dirs.add(util_name)
        
        if len(util_dirs) > 1:
            violations.append(f"Changes affect multiple utility directories: {', '.join(sorted(util_dirs))}")
        
        # Should have no violations
        assert len(violations) == 0
        assert len(util_dirs) == 1
        assert "my-tool" in util_dirs


def test_agent_pr_path_violation_outside_utils():
    """Test that changes outside utils/ directory are detected."""
    
    with patch("agents.agent_utils.get_pr") as mock_get_pr, \
         patch("agents.agent_utils.get_pr_files") as mock_get_files:
        
        mock_get_pr.return_value = {
            "head": {"ref": "ai/gemini-20241205-5678"},
            "state": "open"
        }
        
        mock_get_files.return_value = [
            {"filename": "utils/my-tool/README.md"},
            {"filename": "agents/agent_builder.py"},  # Violation!
        ]
        
        pr = agent_utils.get_pr("owner/repo", 2)
        files = agent_utils.get_pr_files("owner/repo", 2)
        
        # Check if it's an agent PR
        branch = pr.get("head", {}).get("ref", "")
        is_ai_pr = any(branch.startswith(f"ai/{agent}-") for agent in ["gemini", "groq", "openrouter"])
        assert is_ai_pr is True
        
        # Validate paths
        changed_files = [f.get("filename", "") for f in files]
        violations = []
        
        for filepath in changed_files:
            if not filepath.startswith("utils/"):
                violations.append(f"File outside utils/: {filepath}")
        
        # Should have violation
        assert len(violations) == 1
        assert "agents/agent_builder.py" in violations[0]


def test_agent_pr_path_violation_multiple_utils():
    """Test that changes spanning multiple utils directories are detected."""
    
    with patch("agents.agent_utils.get_pr") as mock_get_pr, \
         patch("agents.agent_utils.get_pr_files") as mock_get_files:
        
        mock_get_pr.return_value = {
            "head": {"ref": "ai/openrouter-20241205-9999"},
            "state": "open"
        }
        
        mock_get_files.return_value = [
            {"filename": "utils/tool-a/README.md"},
            {"filename": "utils/tool-b/README.md"},  # Different directory!
        ]
        
        pr = agent_utils.get_pr("owner/repo", 3)
        files = agent_utils.get_pr_files("owner/repo", 3)
        
        # Check if it's an agent PR
        branch = pr.get("head", {}).get("ref", "")
        is_ai_pr = any(branch.startswith(f"ai/{agent}-") for agent in ["gemini", "groq", "openrouter"])
        assert is_ai_pr is True
        
        # Validate paths
        changed_files = [f.get("filename", "") for f in files]
        util_dirs = set()
        violations = []
        
        for filepath in changed_files:
            if not filepath.startswith("utils/"):
                violations.append(f"File outside utils/: {filepath}")
            else:
                parts = filepath.split("/")
                if len(parts) >= 2:
                    util_name = parts[1]
                    util_dirs.add(util_name)
        
        if len(util_dirs) > 1:
            violations.append(f"Changes affect multiple utility directories: {', '.join(sorted(util_dirs))}")
        
        # Should have violation
        assert len(violations) == 1
        assert "tool-a" in violations[0]
        assert "tool-b" in violations[0]
        assert len(util_dirs) == 2


def test_non_agent_pr_is_ignored():
    """Test that non-agent PRs are not checked."""
    
    with patch("agents.agent_utils.get_pr") as mock_get_pr:
        
        mock_get_pr.return_value = {
            "head": {"ref": "feature/my-feature"},
            "state": "open"
        }
        
        pr = agent_utils.get_pr("owner/repo", 4)
        
        # Check if it's an agent PR
        branch = pr.get("head", {}).get("ref", "")
        is_ai_pr = any(branch.startswith(f"ai/{agent}-") for agent in ["gemini", "groq", "openrouter"])
        
        # Should not be an agent PR
        assert is_ai_pr is False
