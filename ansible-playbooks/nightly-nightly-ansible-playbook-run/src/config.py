"""Configuration management for the Ansible Playbook Runner."""

import os
import yaml
from typing import Dict, Any

class ConfigManager:
    """Handle configuration loading and validation."""
    
    DEFAULT_CONFIG = {
        'runner': {
            'default_timeout': 600,
            'enable_rollback': True,
            'report_format': 'html',
            'log_level': 'INFO'
        },
        'validation': {
            'check_syntax': True,
            'check_idempotency': True,
            'check_dependencies': True
        },
        'environments': {}
    }
    
    def __init__(self, config_path: str = 'config.yml'):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or return defaults."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    user_config = yaml.safe_load(f)
                    return self._merge_configs(self.DEFAULT_CONFIG, user_config)
            except Exception as e:
                print(f"Warning: Failed to load config from {self.config_path}: {e}")
        
        return self.DEFAULT_CONFIG.copy()
    
    def _merge_configs(self, base: Dict, override: Dict) -> Dict:
        """Recursively merge configuration dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation."""
        keys = key_path.split('.')
        current = self.config
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        
        return current
    
    def set(self, key_path: str, value: Any) -> None:
        """Set a configuration value using dot notation."""
        keys = key_path.split('.')
        current = self.config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def save(self) -> None:
        """Save current configuration to file."""
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def validate(self) -> tuple[bool, list[str]]:
        """Validate configuration structure."""
        errors = []
        
        # Validate runner section
        runner = self.config.get('runner', {})
        if not isinstance(runner, dict):
            errors.append("runner section must be a dictionary")
        
        if 'default_timeout' in runner:
            if not isinstance(runner['default_timeout'], int) or runner['default_timeout'] <= 0:
                errors.append("runner.default_timeout must be a positive integer")
        
        if 'log_level' in runner:
            valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            if runner['log_level'] not in valid_levels:
                errors.append(f"runner.log_level must be one of {valid_levels}")
        
        # Validate validation section
        validation = self.config.get('validation', {})
        if not isinstance(validation, dict):
            errors.append("validation section must be a dictionary")
        
        # Validate environments section
        environments = self.config.get('environments', {})
        if not isinstance(environments, dict):
            errors.append("environments section must be a dictionary")
        
        return len(errors) == 0, errors
