import json
import os
import tempfile
import unittest
from unittest.mock import Mock, patch, call

import yaml

# Mock rationale: We need to test the validator without requiring actual Ansible installation
from src.validate_playbooks import PlaybookValidator


class TestPlaybookValidator(unittest.TestCase):
    """Test cases for PlaybookValidator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = PlaybookValidator()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_playbook(self, content: dict, filename: str = 'test_playbook.yml') -> str:
        """Create a test playbook file."""
        playbook_path = os.path.join(self.temp_dir, filename)
        with open(playbook_path, 'w') as f:
            yaml.dump(content, f)
        return playbook_path
    
    def test_validate_syntax_valid_playbook(self):
        """Test syntax validation with a valid playbook."""
        playbook_content = [
            {
                'name': 'Test Play',
                'hosts': 'localhost',
                'tasks': [
                    {
                        'name': 'Test Task',
                        'debug': {
                            'msg': 'Hello World'
                        }
                    }
                ]
            }
        ]
        
        playbook_path = self.create_test_playbook(playbook_content)
        result = self.validator.validate_syntax(playbook_path)
        
        self.assertTrue(result['valid'])
        self.assertEqual(result['tasks_count'], 1)
        self.assertEqual(len(result['errors']), 0)
        self.assertEqual(len(result['warnings']), 0)
    
    def test_validate_syntax_invalid_yaml(self):
        """Test syntax validation with invalid YAML."""
        playbook_path = os.path.join(self.temp_dir, 'invalid.yml')
        with open(playbook_path, 'w') as f:
            f.write('invalid: yaml: content: [')  # Invalid YAML
        
        result = self.validator.validate_syntax(playbook_path)
        
        self.assertFalse(result['valid'])
        self.assertGreater(len(result['errors']), 0)
        self.assertIn('YAML syntax error', result['errors'][0])
    
    def test_validate_syntax_missing_tasks(self):
        """Test syntax validation with missing tasks."""
        playbook_content = [
            {
                'name': 'Test Play',
                'hosts': 'localhost'
                # Missing tasks
            }
        ]
        
        playbook_path = self.create_test_playbook(playbook_content)
        result = self.validator.validate_syntax(playbook_path)
        
        self.assertTrue(result['valid'])  # Still valid YAML
        self.assertEqual(result['tasks_count'], 0)
        self.assertEqual(len(result['warnings']), 1)
        self.assertIn('No tasks found', result['warnings'][0])
    
    def test_validate_syntax_deprecated_with_items(self):
        """Test syntax validation detects deprecated with_items."""
        playbook_content = [
            {
                'name': 'Test Play',
                'hosts': 'localhost',
                'tasks': [
                    {
                        'name': 'Test Task',
                        'debug': {'msg': 'test'},
                        'with_items': ['item1', 'item2']
                    }
                ]
            }
        ]
        
        playbook_path = self.create_test_playbook(playbook_content)
        result = self.validator.validate_syntax(playbook_path)
        
        self.assertTrue(result['valid'])
        self.assertEqual(len(result['warnings']), 1)
        self.assertIn('with_items', result['warnings'][0])
    
    @patch('subprocess.run')
    def test_validate_idempotency_success(self, mock_subprocess):
        """Test idempotency validation with successful runs."""
        # Mock successful ansible-playbook runs
        mock_subprocess.return_value = Mock(
            returncode=0,
            stdout='[\n  {\n    "changed": false\n  }\n]',
            stderr=''
        )
        
        playbook_content = [
            {
                'name': 'Test Play',
                'hosts': 'localhost',
                'tasks': [
                    {
                        'name': 'Test Task',
                        'debug': {'msg': 'Hello World'}
                    }
                ]
            }
        ]
        
        playbook_path = self.create_test_playbook(playbook_content)
        result = self.validator.validate_idempotency(playbook_path)
        
        self.assertTrue(result['idempotent'])
        self.assertEqual(result['changes_first_run'], 0)
        self.assertEqual(result['changes_second_run'], 0)
        self.assertEqual(len(result['errors']), 0)
    
    @patch('subprocess.run')
    def test_validate_idempotency_non_idempotent(self, mock_subprocess):
        """Test idempotency validation with non-idempotent playbook."""
        # Mock first run with changes, second run with changes
        mock_subprocess.side_effect = [
            Mock(returncode=0, stdout='[\n  {\n    "changed": true\n  }\n]', stderr=''),
            Mock(returncode=0, stdout='[\n  {\n    "changed": true\n  }\n]', stderr='')
        ]
        
        playbook_content = [
            {
                'name': 'Test Play',
                'hosts': 'localhost',
                'tasks': [
                    {
                        'name': 'Test Task',
                        'debug': {'msg': 'Hello World'}
                    }
                ]
            }
        ]
        
        playbook_path = self.create_test_playbook(playbook_content)
        result = self.validator.validate_idempotency(playbook_path)
        
        self.assertFalse(result['idempotent'])
        self.assertEqual(result['changes_first_run'], 1)
        self.assertEqual(result['changes_second_run'], 1)
        self.assertEqual(len(result['warnings']), 1)
    
    def test_validate_best_practices_good_playbook(self):
        """Test best practices validation with good playbook."""
        playbook_content = [
            {
                'name': 'Test Play',
                'hosts': 'localhost',
                'tasks': [
                    {
                        'name': 'Test Task',
                        'debug': {'msg': 'Hello World'}
                    }
                ]
            }
        ]
        
        playbook_path = self.create_test_playbook(playbook_content)
        result = self.validator.validate_best_practices(playbook_path)
        
        self.assertGreater(result['score'], 0)
        self.assertEqual(len(result['violations']), 0)
        self.assertGreater(result['max_score'], 0)
    
    def test_validate_best_practices_missing_names(self):
        """Test best practices validation with missing names."""
        playbook_content = [
            {
                # Missing play name
                'hosts': 'localhost',
                'tasks': [
                    {
                        # Missing task name
                        'debug': {'msg': 'Hello World'}
                    }
                ]
            }
        ]
        
        playbook_path = self.create_test_playbook(playbook_content)
        result = self.validator.validate_best_practices(playbook_path)
        
        self.assertEqual(result['score'], 0)
        self.assertGreater(len(result['violations']), 0)
        self.assertIn('Missing play name', result['violations'][0])
        self.assertIn('Missing task name', result['violations'][1])
    
    def test_validate_best_practices_recommendations(self):
        """Test best practices validation provides recommendations."""
        playbook_content = [
            {
                'name': 'Test Play',
                'hosts': 'localhost',
                'tasks': [
                    {
                        'name': 'Test Task',
                        'copy': {
                            'src': 'template.j2',
                            'dest': '/tmp/file'
                        }
                    }
                ]
            }
        ]
        
        playbook_path = self.create_test_playbook(playbook_content)
        result = self.validator.validate_best_practices(playbook_path)
        
        self.assertGreater(len(result['recommendations']), 0)
        self.assertIn('template module', result['recommendations'][0])
    
    def test_generate_report(self):
        """Test HTML report generation."""
        # Add some test results
        self.validator.validation_results['syntax'] = [
            {
                'file': 'test.yml',
                'valid': True,
                'errors': [],
                'warnings': [],
                'tasks_count': 2
            }
        ]
        self.validator.validation_results['idempotency'] = [
            {
                'file': 'test.yml',
                'idempotent': True,
                'changes_first_run': 0,
                'changes_second_run': 0,
                'errors': [],
                'warnings': []
            }
        ]
        self.validator.validation_results['best_practices'] = [
            {
                'file': 'test.yml',
                'score': 5,
                'max_score': 5,
                'violations': [],
                'recommendations': []
            }
        ]
        
        # Test report generation
        html_content = self.validator.generate_report()
        
        self.assertIn('<title>Ansible Playbook Validation Report</title>', html_content)
        self.assertIn('test.yml', html_content)
        self.assertIn('✅ Valid', html_content)
        self.assertIn('✅ Idempotent', html_content)
    
    def test_generate_report_to_file(self):
        """Test HTML report generation to file."""
        report_path = os.path.join(self.temp_dir, 'test_report.html')
        result = self.validator.generate_report(report_path)
        
        self.assertIn('Report generated', result)
        self.assertTrue(os.path.exists(report_path))
        
        with open(report_path, 'r') as f:
            content = f.read()
            self.assertIn('<title>Ansible Playbook Validation Report</title>', content)


class TestCommandLineInterface(unittest.TestCase):
    """Test command-line interface."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_playbook(self, content: dict, filename: str = 'test_playbook.yml') -> str:
        """Create a test playbook file."""
        playbook_path = os.path.join(self.temp_dir, filename)
        with open(playbook_path, 'w') as f:
            yaml.dump(content, f)
        return playbook_path
    
    @patch('sys.argv', ['validate_playbooks.py', 'validate', 'test.yml'])
    @patch('src.validate_playbooks.PlaybookValidator')
    def test_main_validate_command(self, mock_validator_class):
        """Test main function with validate command."""
        mock_validator = Mock()
        mock_validator_class.return_value = mock_validator
        
        # Mock file existence check
        with patch('os.path.exists', return_value=True):
            # Mock validation methods
            mock_validator.validate_syntax.return_value = {'valid': True, 'tasks_count': 1, 'errors': [], 'warnings': []}
            mock_validator.validate_idempotency.return_value = {'idempotent': True, 'changes_first_run': 0, 'changes_second_run': 0, 'errors': [], 'warnings': []}
            mock_validator.validate_best_practices.return_value = {'score': 5, 'max_score': 5, 'violations': [], 'recommendations': []}
            
            # This would normally call sys.exit, so we catch it
            try:
                from src.validate_playbooks import main
                main()
            except SystemExit:
                pass
        
        # Verify validator methods were called
        mock_validator.validate_syntax.assert_called_once()
        mock_validator.validate_idempotency.assert_called_once()
        mock_validator.validate_best_practices.assert_called_once()
    
    @patch('sys.argv', ['validate_playbooks.py', 'report', '--output', 'test_report.html'])
    @patch('src.validate_playbooks.PlaybookValidator')
    def test_main_report_command(self, mock_validator_class):
        """Test main function with report command."""
        mock_validator = Mock()
        mock_validator_class.return_value = mock_validator
        mock_validator.generate_report.return_value = 'Report generated: test_report.html'
        
        try:
            from src.validate_playbooks import main
            main()
        except SystemExit:
            pass
        
        mock_validator.generate_report.assert_called_once_with('test_report.html')


if __name__ == '__main__':
    unittest.main()
