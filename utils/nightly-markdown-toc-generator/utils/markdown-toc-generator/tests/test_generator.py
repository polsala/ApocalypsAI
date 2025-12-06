import importlib.util
import pathlib


def _load_generator_module():
    """Load the generator module from the sibling src directory without using package imports."""
    src_path = pathlib.Path(__file__).resolve().parents[1] / "src" / "generator.py"
    spec = importlib.util.spec_from_file_location("generator", src_path)
    module = importlib.util.module_from_spec(spec)
    # Mock rationale: loading module directly ensures tests stay offline and deterministic.
    spec.loader.exec_module(module)
    return module


def test_generate_toc_basic():
    gen = _load_generator_module()
    md = """# Project
## Installation
## Usage
### Advanced Features
# Appendix
"""
    expected = """- [Project](#project)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Advanced Features](#advanced-features)
- [Appendix](#appendix)"""
    assert gen.generate_toc(md) == expected


def test_generate_toc_no_headings():
    gen = _load_generator_module()
    md = "Just a plain paragraph without headings."
    assert gen.generate_toc(md) == ""


def test_slugify_special_chars():
    gen = _load_generator_module()
    md = "# C++ & Python: The \"Best\" Languages!"
    expected = "- [C++ & Python: The \"Best\" Languages!](#c--python-the-best-languages)"
    assert gen.generate_toc(md) == expected
