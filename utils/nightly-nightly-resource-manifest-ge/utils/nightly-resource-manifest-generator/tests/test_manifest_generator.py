import pytest
import os
from unittest.mock import patch, mock_open
from datetime import datetime
from src.manifest_generator import generate_manifest, parse_requirements_txt, parse_package_json, parse_go_mod, parse_cargo_toml

# Mock rationale: os.walk, os.path.join, and open are filesystem operations.
# To ensure deterministic and offline tests, these need to be mocked to simulate
# different directory structures and file contents without touching the actual disk.
# datetime.utcnow is mocked to ensure consistent timestamp in the output.
# The 'toml' library is mocked to control its parsing behavior without actual file I/O.

@pytest.fixture
def mock_filesystem():
    """Fixture to mock os.walk, os.path.join, builtins.open, toml, and datetime."""
    with patch('os.walk') as mock_walk, \
         patch('os.path.join', side_effect=os.path.join), \
         patch('builtins.open', new_callable=mock_open) as mock_file_open, \
         patch('src.manifest_generator.toml', autospec=True) as mock_toml, \
         patch('src.manifest_generator.datetime') as mock_datetime:
        
        mock_datetime.utcnow.return_value = datetime(2023, 10, 27, 10, 30, 0)
        mock_datetime.strftime.return_value = "2023-10-27 10:30:00 UTC"
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw) # Allow datetime to be called for other purposes

        yield mock_walk, mock_file_open, mock_toml

def test_parse_requirements_txt():
    mock_content = "requests==2.28.1\n# A comment\npyyaml>=6.0\n\nrich~=13.0"
    m = mock_open(read_data=mock_content)
    with patch('builtins.open', m):
        deps = parse_requirements_txt("dummy/requirements.txt")
        assert deps == ["requests==2.28.1", "pyyaml>=6.0", "rich~=13.0"]

def test_parse_package_json():
    mock_content = """
    {
      "name": "my-app",
      "version": "1.0.0",
      "dependencies": {
        "express": "^4.18.2",
        "lodash": "~4.17.21"
      },
      "devDependencies": {
        "jest": "^29.0.0"
      }
    }
    """
    m = mock_open(read_data=mock_content)
    with patch('builtins.open', m):
        deps = parse_package_json("dummy/package.json")
        assert sorted(deps) == sorted(["express: ^4.18.2", "lodash: ~4.17.21", "jest: ^29.0.0"])

def test_parse_go_mod():
    mock_content = """
    module example.com/my-go-app

    go 1.19

    require (
        github.com/gin-gonic/gin v1.8.1
        golang.org/x/text v0.3.7 // indirect
    )

    require github.com/stretchr/testify v1.8.0
    """
    m = mock_open(read_data=mock_content)
    with patch('builtins.open', m):
        deps = parse_go_mod("dummy/go.mod")
        assert sorted(deps) == sorted([
            "github.com/gin-gonic/gin v1.8.1",
            "golang.org/x/text v0.3.7",
            "github.com/stretchr/testify v1.8.0"
        ])

def test_parse_cargo_toml(mock_filesystem):
    _, mock_file_open, mock_toml = mock_filesystem
    mock_content = """
    [package]
    name = "my-rust-app"
    version = "0.1.0"

    [dependencies]
    serde = "1.0"
    tokio = { version = "1.20", features = ["full"] }
    rand = { git = "https://github.com/rust-random/rand.git", branch = "master" }
    """
    mock_file_open.return_value.__enter__.return_value.read.return_value = mock_content
    mock_toml.load.return_value = {
        "package": {"name": "my-rust-app", "version": "0.1.0"},
        "dependencies": {
            "serde": "1.0",
            "tokio": {"version": "1.20", "features": ["full"]},
            "rand": {"git": "https://github.com/rust-random/rand.git", "branch": "master"}
        }
    }
    
    deps = parse_cargo_toml("dummy/Cargo.toml")
    assert sorted(deps) == sorted([
        'serde = "1.0"',
        'tokio = { features = ["full"], version = "1.20" }',
        'rand = { branch = "master", git = "https://github.com/rust-random/rand.git" }'
    ])


def test_generate_manifest_empty_project(mock_filesystem):
    mock_walk, mock_file_open, _ = mock_filesystem
    mock_walk.return_value = [
        ('/project', [], ['main.py'])
    ]
    
    output_path = "/output/manifest.md"
    generate_manifest("/project", output_path)

    expected_output = """# Project Resource Manifest\n\nGenerated on: 2023-10-27 10:30:00 UTC\n"""
    mock_file_open.assert_called_once_with(output_path, 'w')
    mock_file_open().write.assert_called_once_with(expected_output)

def test_generate_manifest_single_language_project(mock_filesystem):
    mock_walk, mock_file_open, _ = mock_filesystem
    mock_walk.return_value = [
        ('/project', ['src'], ['README.md']),
        ('/project/src', [], ['requirements.txt'])
    ]
    mock_file_open.side_effect = [
        mock_open(read_data="requests==2.28.1\npyyaml>=6.0").return_value, # For requirements.txt
        mock_open().return_value # For output file
    ]
    
    output_path = "/output/manifest.md"
    generate_manifest("/project", output_path)

    expected_output = """# Project Resource Manifest\n\nGenerated on: 2023-10-27 10:30:00 UTC\n\n## Python Dependencies\n\n*   pyyaml>=6.0\n*   requests==2.28.1\n"""
    mock_file_open.assert_called_with(output_path, 'w')
    mock_file_open().write.assert_called_with(expected_output)

def test_generate_manifest_multi_language_project(mock_filesystem):
    mock_walk, mock_file_open, mock_toml = mock_filesystem
    mock_walk.return_value = [
        ('/project', ['backend', 'frontend'], []),
        ('/project/backend', [], ['requirements.txt', 'go.mod']),
        ('/project/frontend', [], ['package.json', 'Cargo.toml'])
    ]
    
    # Define file contents
    file_contents = {
        os.path.join('/project/backend', 'requirements.txt'): "requests==2.28.1\nflask==2.0.0",
        os.path.join('/project/backend', 'go.mod'): "module example.com/go\nrequire github.com/gin-gonic/gin v1.8.1",
        os.path.join('/project/frontend', 'package.json'): '{"dependencies": {"react": "^17.0.2"}}',
        os.path.join('/project/frontend', 'Cargo.toml'): '[dependencies]\nserde = "1.0"'
    }

    # Configure mock_open to return specific content for specific files
    def mock_open_for_read(file_path, mode='r', *args, **kwargs):
        if mode == 'r' and file_path in file_contents:
            return mock_open(read_data=file_contents[file_path]).return_value
        elif mode == 'w':
            return mock_open().return_value # For the output file
        raise FileNotFoundError(f"File not found for mock: {file_path}")

    mock_file_open.side_effect = mock_open_for_read

    # Configure mock_toml.load for Cargo.toml
    mock_toml.load.return_value = {'dependencies': {'serde': '1.0'}}

    output_path = "/output/manifest.md"
    generate_manifest("/project", output_path)

    expected_output = """# Project Resource Manifest\n\nGenerated on: 2023-10-27 10:30:00 UTC\n\n## Go Dependencies\n\n*   github.com/gin-gonic/gin v1.8.1\n\n## Node.js Dependencies\n\n*   react: ^17.0.2\n\n## Python Dependencies\n\n*   flask==2.0.0\n*   requests==2.28.1\n\n## Rust Dependencies\n\n*   serde = \"1.0\"\n"""
    mock_file_open.assert_called_with(output_path, 'w')
    mock_file_open().write.assert_called_with(expected_output)

def test_generate_manifest_handles_duplicates(mock_filesystem):
    mock_walk, mock_file_open, _ = mock_filesystem
    mock_walk.return_value = [
        ('/project', [], ['requirements.txt'])
    ]
    mock_file_open.side_effect = [
        mock_open(read_data="requests==2.28.1\nrequests==2.28.1\npyyaml>=6.0").return_value, # For requirements.txt
        mock_open().return_value # For output file
    ]
    
    output_path = "/output/manifest.md"
    generate_manifest("/project", output_path)

    expected_output = """# Project Resource Manifest\n\nGenerated on: 2023-10-27 10:30:00 UTC\n\n## Python Dependencies\n\n*   pyyaml>=6.0\n*   requests==2.28.1\n"""
    mock_file_open.assert_called_with(output_path, 'w')
    mock_file_open().write.assert_called_with(expected_output)

def test_generate_manifest_handles_parsing_errors(mock_filesystem):
    mock_walk, mock_file_open, _ = mock_filesystem
    mock_walk.return_value = [
        ('/project', [], ['package.json'])
    ]
    # Malformed JSON
    mock_file_open.side_effect = [
        mock_open(read_data="{'dependencies': {'react': '^17.0.2'}").return_value, # For package.json (invalid JSON)
        mock_open().return_value # For output file
    ]
    
    output_path = "/output/manifest.md"
    generate_manifest("/project", output_path)

    # Expect an empty dependencies section for Node.js if parsing fails
    expected_output = """# Project Resource Manifest\n\nGenerated on: 2023-10-27 10:30:00 UTC\n"""
    mock_file_open.assert_called_with(output_path, 'w')
    mock_file_open().write.assert_called_with(expected_output)
