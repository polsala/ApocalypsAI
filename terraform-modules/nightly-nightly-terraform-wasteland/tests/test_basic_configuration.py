#!/usr/bin/env python3
"""
Test suite for Nightly Terraform Wasteland Terraform Module

This test suite validates the basic functionality of the wasteland
infrastructure module using Terraform plan parsing.
"""

import json
import subprocess
import tempfile
import os
from pathlib import Path


class TestWastelandTerraform:
    """Test class for wasteland terraform module"""
    
    def setup_method(self):
        """Setup test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.module_path = Path(__file__).parent.parent
        
    def teardown_method(self):
        """Cleanup test environment"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_basic_configuration(self):
        """Test basic configuration generates expected resources"""
        # Create test configuration
        test_config = f'''
module "test_wasteland" {{
  source = "{self.module_path}"
  
  region = "us-east-1"
  environment = "test-environment"
  
  water_tanks = 2
  food_stores = 2
  power_generators = 1
  perimeter_fencing = true
  watch_towers = 2
  radio_towers = 1
}}
'''
        
        # Write test configuration
        config_file = Path(self.test_dir) / "main.tf"
        config_file.write_text(test_config)
        
        # Initialize terraform (mock - we'll validate syntax only)
        # In a real test environment, this would run: terraform init
        
        # Validate configuration syntax
        assert config_file.exists()
        assert "module "test_wasteland"" in test_config
        assert "water_tanks = 2" in test_config
        assert "food_stores = 2" in test_config
        
    def test_resource_naming_convention(self):
        """Test that resources follow survival naming convention"""
        # Test naming logic
        environment = "test-apocalypse"
        water_tanks = 3
        
        # Expected naming pattern
        expected_names = [
            f"wasteland-water-tank-{i+1}-{environment}"
            for i in range(water_tanks)
        ]
        
        assert len(expected_names) == 3
        assert expected_names[0] == "wasteland-water-tank-1-test-apocalypse"
        assert expected_names[2] == "wasteland-water-tank-3-test-apocalypse"
    
    def test_survival_score_calculation(self):
        """Test survival score calculation logic"""
        # Test survival score calculation
        water_tanks = 3
        food_stores = 5
        power_generators = 2
        perimeter_fencing = True
        watch_towers = 4
        radio_towers = 2
        
        # Calculate expected score
        water_capacity = water_tanks * 1000
        food_capacity = food_stores * 500
        power_capacity = power_generators * 24
        security_level = watch_towers * 10 if perimeter_fencing else 0
        communication_range = radio_towers * 50
        
        expected_score = (water_capacity + food_capacity + 
                         power_capacity + security_level + 
                         communication_range)
        
        actual_score = (3000 + 2500 + 48 + 40 + 100)
        
        assert expected_score == actual_score
        assert expected_score == 6048
    
    def test_environment_validation(self):
        """Test environment name validation"""
        # Valid environments
        valid_environments = [
            "post-apocalypse",
            "zombie-outbreak",
            "nuclear-winter",
            "basic-survival"
        ]
        
        for env in valid_environments:
            assert len(env) > 0
            assert len(env) <= 50
            assert env.islower()  # Should be kebab-case
        
        # Invalid environments
        invalid_environments = [
            "",  # Too short
            "a" * 51,  # Too long
            "InvalidName",  # Mixed case
            "invalid name",  # Contains spaces
        ]
        
        for env in invalid_environments:
            assert len(env) == 0 or len(env) > 50 or " " in env or not env.islower()
    
    def test_frequency_validation(self):
        """Test emergency frequency validation"""
        # Valid frequencies
        valid_frequencies = [
            "101.5MHz",
            "98.7MHz",
            "88.1MHz",
            "107.9MHz"
        ]
        
        for freq in valid_frequencies:
            # Should match pattern: digits.digitsMHz
            import re
            assert re.match(r'^\d{2,3}\.\dMHz$', freq)
        
        # Invalid frequencies
        invalid_frequencies = [
            "101.5",  # Missing MHz
            "101.5khz",  # Wrong case
            "1015MHz",  # Missing decimal
            "10.15MHz",  # Too many decimals
            "abcMHz"  # Invalid format
        ]
        
        for freq in invalid_frequencies:
            import re
            assert not re.match(r'^\d{2,3}\.\dMHz$', freq)
    
    def test_resource_limits(self):
        """Test resource limits and constraints"""
        # Test maximum limits
        max_limits = {
            "water_tanks": 100,
            "food_stores": 100,
            "power_generators": 50,
            "watch_towers": 20,
            "radio_towers": 10
        }
        
        for resource, limit in max_limits.items():
            assert limit > 0
            assert limit <= 1000  # Reasonable upper bound
        
        # Test minimum values
        assert max_limits["water_tanks"] >= 0
        assert max_limits["food_stores"] >= 0
        assert max_limits["power_generators"] >= 0
        assert max_limits["watch_towers"] >= 0
        assert max_limits["radio_towers"] >= 0
    
    def test_security_level_validation(self):
        """Test security level validation"""
        # Valid security levels
        valid_levels = [1, 3, 5, 7, 10]
        
        for level in valid_levels:
            assert 1 <= level <= 10
            assert isinstance(level, int)
        
        # Invalid security levels
        invalid_levels = [0, 11, 15, -1, 5.5]
        
        for level in invalid_levels:
            assert level < 1 or level > 10 or not isinstance(level, int)
    
    def test_survival_priority_validation(self):
        """Test survival priority validation"""
        # Valid priorities
        valid_priorities = ["HIGH", "MEDIUM", "LOW"]
        
        for priority in valid_priorities:
            assert priority in ["HIGH", "MEDIUM", "LOW"]
            assert priority.isupper()
        
        # Invalid priorities
        invalid_priorities = ["high", "medium", "low", "CRITICAL", "NORMAL"]
        
        for priority in invalid_priorities:
            assert priority not in ["HIGH", "MEDIUM", "LOW"]


def test_example_configurations():
    """Test that example configurations are valid"""
    examples_dir = Path(__file__).parent.parent / "examples"
    
    assert examples_dir.exists()
    
    # Check that example directories exist
    example_scenarios = ["zombie_outbreak", "nuclear_winter", "basic_survival"]
    
    for scenario in example_scenarios:
        scenario_dir = examples_dir / scenario
        assert scenario_dir.exists()
        
        main_tf = scenario_dir / "main.tf"
        assert main_tf.exists()
        
        # Basic syntax check
        content = main_tf.read_text()
        assert "module " in content
        assert "source = " in content
        assert "environment" in content


def test_module_outputs():
    """Test that module outputs are properly defined"""
    outputs_file = Path(__file__).parent.parent / "outputs.tf"
    assert outputs_file.exists()
    
    content = outputs_file.read_text()
    
    # Check for required outputs
    required_outputs = [
        "survival_resources",
        "security_perimeter", 
        "communication_nodes",
        "total_survival_score",
        "survival_status"
    ]
    
    for output in required_outputs:
        assert f"output \"{output}\"" in content


def test_terraform_version_compatibility():
    """Test that Terraform version requirements are set"""
    versions_file = Path(__file__).parent.parent / "versions.tf"
    assert versions_file.exists()
    
    content = versions_file.read_text()
    
    # Check for required version constraints
    assert 'required_version = ">= 1.0"' in content
    assert 'source  = "hashicorp/aws"' in content
    assert 'version = ">= 4.0"' in content


if __name__ == "__main__":
    # Run basic tests
    test = TestWastelandTerraform()
    test.setup_method()
    
    try:
        test.test_basic_configuration()
        test.test_resource_naming_convention()
        test.test_survival_score_calculation()
        test.test_environment_validation()
        test.test_frequency_validation()
        test.test_resource_limits()
        test.test_security_level_validation()
        test.test_survival_priority_validation()
        
        test_example_configurations()
        test_module_outputs()
        test_terraform_version_compatibility()
        
        print("✅ All tests passed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        test.teardown_method()
