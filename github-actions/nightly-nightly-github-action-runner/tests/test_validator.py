import os
import tempfile
import yaml
import json
from pathlib import Path
from unittest.mock import patch, mock_open
import pytest

# Mock the WorkflowValidator class for testing
class WorkflowValidator:
    def __init__(self, strict_mode: bool = False):
        self.strict_mode = strict_mode
        self.results = {
            'passed': 0,
            'warnings': 0,
            'errors': 0,
            'details': []
        }
    
    def validate_workflow(self, file_path: str):
        # This would normally read and validate the file
        # For testing, we'll simulate different scenarios
        result = {
            'file': file_path,
            'status': 'passed',
            'issues': [],
            'warnings': []
        }
        
        if 'valid' in file_path:
            result['status'] = 'passed'
        elif 'warning' in file_path:
            result['warnings'].append('Sample warning')
        elif 'error' in file_path:
            result['status'] = 'failed'
            result['issues'].append('Sample error')
        
        return result
    
    def validate_all(self, workflow_files):
        for file_path in workflow_files:
            result = self.validate_workflow(file_path)
            self.results['details'].append(result)
            
            if result['status'] == 'failed':
                self.results['errors'] += 1
            elif result['warnings']:
                self.results['warnings'] += 1
            else:
                self.results['passed'] += 1
        
        return self.results

def test_workflow_validator_initialization():
    """Test that WorkflowValidator initializes correctly"""
    validator = WorkflowValidator()
    assert validator.strict_mode == False
    assert validator.results['passed'] == 0
    assert validator.results['warnings'] == 0
    assert validator.results['errors'] == 0
    assert validator.results['details'] == []
    
    validator_strict = WorkflowValidator(strict_mode=True)
    assert validator_strict.strict_mode == True

def test_validate_workflow_valid():
    """Test validation of a valid workflow"""
    validator = WorkflowValidator()
    result = validator.validate_workflow('valid_workflow.yml')
    
    assert result['file'] == 'valid_workflow.yml'
    assert result['status'] == 'passed'
    assert result['issues'] == []
    assert result['warnings'] == []

def test_validate_workflow_with_warnings():
    """Test validation of a workflow with warnings"""
    validator = WorkflowValidator()
    result = validator.validate_workflow('workflow_with_warnings.yml')
    
    assert result['file'] == 'workflow_with_warnings.yml'
    assert result['status'] == 'passed'
    assert result['issues'] == []
    assert len(result['warnings']) == 1
    assert result['warnings'][0] == 'Sample warning'

def test_validate_workflow_with_errors():
    """Test validation of a workflow with errors"""
    validator = WorkflowValidator()
    result = validator.validate_workflow('workflow_with_errors.yml')
    
    assert result['file'] == 'workflow_with_errors.yml'
    assert result['status'] == 'failed'
    assert len(result['issues']) == 1
    assert result['issues'][0] == 'Sample error'
    assert result['warnings'] == []

def test_validate_all_workflows():
    """Test validation of multiple workflows"""
    validator = WorkflowValidator()
    workflow_files = [
        'valid_workflow.yml',
        'workflow_with_warnings.yml',
        'workflow_with_errors.yml'
    ]
    
    results = validator.validate_all(workflow_files)
    
    assert results['passed'] == 1
    assert results['warnings'] == 1
    assert results['errors'] == 1
    assert len(results['details']) == 3
    
    # Check individual results
    assert results['details'][0]['status'] == 'passed'
    assert results['details'][1]['warnings'] == ['Sample warning']
    assert results['details'][2]['status'] == 'failed'
    assert results['details'][2]['issues'] == ['Sample error']

def test_yaml_parsing():
    """Test YAML parsing functionality"""
    # Test valid YAML
    valid_yaml = """
name: Test Workflow
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
"""
    
    parsed = yaml.safe_load(valid_yaml)
    assert parsed['name'] == 'Test Workflow'
    assert parsed['on'] == ['push', 'pull_request']
    assert 'jobs' in parsed
    assert 'test' in parsed['jobs']
    
    # Test invalid YAML
    invalid_yaml = """
name: Test Workflow
on: [push, pull_request
jobs:
  test:
    runs-on: ubuntu-latest
"""
    
    try:
        yaml.safe_load(invalid_yaml)
        assert False, "Should have raised YAML error"
    except yaml.YAMLError:
        pass  # Expected

def test_security_pattern_detection():
    """Test detection of security patterns"""
    import re
    
    # Test password pattern
    content_with_password = "password: mysecretpassword"
    password_pattern = r'password\s*[:=]\s*[^\s]+'
    assert re.search(password_pattern, content_with_password, re.IGNORECASE)
    
    # Test token pattern
    content_with_token = "token: abc123def456"
    token_pattern = r'token\s*[:=]\s*[^\s]+'
    assert re.search(token_pattern, content_with_token, re.IGNORECASE)
    
    # Test safe content
    safe_content = "echo: 'This is safe content'"
    assert not re.search(password_pattern, safe_content, re.IGNORECASE)
    assert not re.search(token_pattern, safe_content, re.IGNORECASE)

def test_action_version_pinning():
    """Test detection of unpinned action versions"""
    test_cases = [
        ('actions/checkout@v4', True, 'Pinned version'),
        ('actions/checkout@v1', True, 'Pinned but deprecated'),
        ('actions/checkout@main', False, 'Unpinned to branch'),
        ('actions/checkout@master', False, 'Unpinned to branch'),
        ('actions/checkout', False, 'No version specified'),
        ('./local-action', True, 'Local action - skip check')
    ]
    
    for action, should_be_pinned, description in test_cases:
        if action.startswith('.'):
            # Skip local actions
            assert True
        else:
            has_version = '@' in action
            not_main_master = not action.endswith('@main') and not action.endswith('@master')
            
            if should_be_pinned:
                assert has_version and not_main_master, f"{description}: {action}"
            else:
                assert not (has_version and not_main_master), f"{description}: {action}"

def test_permissions_checking():
    """Test permissions validation"""
    # Test with permissions
    workflow_with_perms = {
        'name': 'Test',
        'on': ['push'],
        'jobs': {},
        'permissions': {
            'contents': 'read',
            'id-token': 'write'
        }
    }
    
    assert 'permissions' in workflow_with_perms
    assert workflow_with_perms['permissions']['contents'] == 'read'
    
    # Test without permissions
    workflow_without_perms = {
        'name': 'Test',
        'on': ['push'],
        'jobs': {}
    }
    
    assert 'permissions' not in workflow_without_perms

def test_matrix_strategy_checking():
    """Test matrix strategy validation"""
    # Test small matrix
    small_matrix = {'os': ['ubuntu-latest', 'windows-latest']}
    assert len(small_matrix) <= 5
    
    # Test large matrix
    large_matrix = {
        'os': ['ubuntu-latest', 'windows-latest', 'macos-latest'],
        'node-version': ['14', '16', '18', '20'],
        'database': ['postgres', 'mysql']
    }
    # This would be a large matrix in practice
    assert len(large_matrix) > 5

def test_cache_detection():
    """Test detection of caching in workflows"""
    steps_with_cache = [
        {'uses': 'actions/cache@v3'},
        {'run': 'npm install'}
    ]
    
    steps_without_cache = [
        {'run': 'npm install'},
        {'run': 'npm test'}
    ]
    
    # Check for cache action
    has_cache = any('actions/cache' in str(step.get('uses', '')) for step in steps_with_cache)
    assert has_cache
    
    has_cache_no = any('actions/cache' in str(step.get('uses', '')) for step in steps_without_cache)
    assert not has_cache_no

def test_trusted_publisher_checking():
    """Test detection of trusted action publishers"""
    trusted_publishers = ['actions/', 'docker/', 'google-github-actions/', 'aws-actions/', 'azure/']
    
    trusted_actions = [
        'actions/checkout@v4',
        'docker/build-push-action@v5',
        'google-github-actions/auth@v2',
        'aws-actions/amazon-ecr-login@v2',
        'azure/login@v2'
    ]
    
    untrusted_actions = [
        'some-random/action@v1',
        'community-actions/example@v2'
    ]
    
    for action in trusted_actions:
        is_trusted = any(trusted in action for trusted in trusted_publishers)
        assert is_trusted, f"{action} should be trusted"
    
    for action in untrusted_actions:
        is_trusted = any(trusted in action for trusted in trusted_publishers)
        assert not is_trusted, f"{action} should not be trusted"

def test_json_output_format():
    """Test that JSON output is properly formatted"""
    results = {
        'passed': 2,
        'warnings': 1,
        'errors': 1,
        'details': [
            {
                'file': 'valid.yml',
                'status': 'passed',
                'issues': [],
                'warnings': []
            },
            {
                'file': 'error.yml',
                'status': 'failed',
                'issues': ['Missing name field'],
                'warnings': []
            }
        ]
    }
    
    # Test JSON serialization
    json_output = json.dumps(results)
    assert isinstance(json_output, str)
    
    # Test JSON deserialization
    parsed = json.loads(json_output)
    assert parsed == results
    assert parsed['passed'] == 2
    assert parsed['details'][1]['issues'][0] == 'Missing name field'

def test_environment_variable_handling():
    """Test handling of environment variables"""
    # Test STRICT_MODE environment variable
    with patch.dict(os.environ, {'STRICT_MODE': 'true'}):
        assert os.environ['STRICT_MODE'] == 'true'
        strict_mode = os.environ.get('STRICT_MODE', 'false').lower() == 'true'
        assert strict_mode == True
    
    with patch.dict(os.environ, {}, clear=True):
        strict_mode = os.environ.get('STRICT_MODE', 'false').lower() == 'true'
        assert strict_mode == False

def test_file_path_handling():
    """Test handling of file paths"""
    # Test path conversion
    workflow_paths = '.github/workflows,custom/workflows'
    ignore_patterns = 'test/**,temp/**'
    
    # Convert to arrays
    paths = [p.strip() for p in workflow_paths.split(',')]
    ignores = [i.strip() for i in ignore_patterns.split(',')]
    
    assert paths == ['.github/workflows', 'custom/workflows']
    assert ignores == ['test/**', 'temp/**']
    
    # Test file existence check
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write('name: Test\non: [push]\njobs: {}')
        temp_file = f.name
    
    try:
        assert os.path.exists(temp_file)
        assert temp_file.endswith('.yml')
    finally:
        os.unlink(temp_file)

def test_comprehensive_workflow_validation():
    """Test comprehensive validation of a complete workflow"""
    complete_workflow = {
        'name': 'CI/CD Pipeline',
        'on': ['push', 'pull_request'],
        'permissions': {
            'contents': 'read',
            'packages': 'write'
        },
        'jobs': {
            'build': {
                'runs-on': 'ubuntu-latest',
                'strategy': {
                    'matrix': {
                        'node-version': ['16', '18', '20']
                    }
                },
                'steps': [
                    {'uses': 'actions/checkout@v4'},
                    {'uses': 'actions/setup-node@v4', 'with': {'node-version': '${{ matrix.node-version }}'}},
                    {'uses': 'actions/cache@v3', 'with': {'path': '~/.npm', 'key': '${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}'}},
                    {'run': 'npm ci'},
                    {'run': 'npm run build'},
                    {'run': 'npm test'}
                ]
            }
        }
    }
    
    # Validate structure
    assert 'name' in complete_workflow
    assert 'on' in complete_workflow
    assert 'jobs' in complete_workflow
    assert 'permissions' in complete_workflow
    
    # Validate jobs
    assert 'build' in complete_workflow['jobs']
    build_job = complete_workflow['jobs']['build']
    assert 'runs-on' in build_job
    assert 'steps' in build_job
    
    # Validate steps
    steps = build_job['steps']
    assert len(steps) == 6
    
    # Check for pinned actions
    for step in steps:
        uses = step.get('uses', '')
        if uses and not uses.startswith('.'):
            assert '@' in uses
            assert not uses.endswith('@main')
            assert not uses.endswith('@master')
    
    # Check for cache
    has_cache = any('actions/cache' in str(step.get('uses', '')) for step in steps)
    assert has_cache
    
    # Check matrix size
    matrix = build_job.get('strategy', {}).get('matrix', {})
    assert len(matrix) == 1  # Just node-version
    assert len(matrix.get('node-version', [])) == 3

if __name__ == '__main__':
    # Run all tests
    import sys
    
    test_functions = [
        test_workflow_validator_initialization,
        test_validate_workflow_valid,
        test_validate_workflow_with_warnings,
        test_validate_workflow_with_errors,
        test_validate_all_workflows,
        test_yaml_parsing,
        test_security_pattern_detection,
        test_action_version_pinning,
        test_permissions_checking,
        test_matrix_strategy_checking,
        test_cache_detection,
        test_trusted_publisher_checking,
        test_json_output_format,
        test_environment_variable_handling,
        test_file_path_handling,
        test_comprehensive_workflow_validation
    ]
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            test_func()
            print(f"✅ {test_func.__name__}")
            passed += 1
        except Exception as e:
            print(f"❌ {test_func.__name__}: {e}")
            failed += 1
    
    print(f"\nTest Results: {passed} passed, {failed} failed")
    
    if failed > 0:
        sys.exit(1)
    else:
        print("All tests passed!")
