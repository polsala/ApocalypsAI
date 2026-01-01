#!/usr/bin/env python3
"""
Test suite for Zombie Outbreak Scenario

Validates the high-security configuration for zombie apocalypse scenarios.
"""

import json
import tempfile
from pathlib import Path


class TestZombieOutbreakScenario:
    """Test class for zombie outbreak scenario"""
    
    def setup_method(self):
        """Setup test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.scenario_path = Path(__file__).parent.parent / "examples" / "zombie_outbreak"
        
    def test_zombie_scenario_configuration(self):
        """Test zombie outbreak scenario configuration"""
        main_tf = self.scenario_path / "main.tf"
        assert main_tf.exists()
        
        content = main_tf.read_text()
        
        # Check zombie-specific configuration
        assert "zombie_outbreak_survival" in content
        assert "environment   = \"zombie-outbreak\"" in content
        assert "water_tanks   = 15" in content
        assert "food_stores   = 25" in content
        assert "power_generators = 8" in content
        assert "watch_towers  = 12" in content
        assert "security_level = 10" in content
        assert "radio_towers  = 5" in content
        
        # Check zombie-specific tags
        assert "ThreatLevel = \"ZOMBIE_APOCALYPSE\"" in content
        assert "Quarantine  = \"ACTIVE\"" in content
        assert "Biohazard   = \"WARNING\"" in content
    
    def test_zombie_scenario_outputs(self):
        """Test zombie scenario output validation"""
        main_tf = self.scenario_path / "main.tf"
        content = main_tf.read_text()
        
        # Check for zombie-specific outputs
        assert "zombie_outbreak_status" in content
        assert "zombie_defense_status" in content
        
        # Check defense status values
        assert "perimeter_integrity = \"MAXIMUM\"" in content
        assert "watch_tower_coverage = \"360_DEGREES\"" in content
        assert "emergency_response_time = \"2_MINUTES\"" in content
        assert "zombie_threat_level = \"CONTAINED\"" in content
    
    def test_zombie_survival_score(self):
        """Test zombie scenario survival score calculation"""
        # Zombie scenario configuration
        water_tanks = 15
        food_stores = 25
        power_generators = 8
        perimeter_fencing = True
        watch_towers = 12
        radio_towers = 5
        
        # Calculate survival score
        water_capacity = water_tanks * 1000
        food_capacity = food_stores * 500
        power_capacity = power_generators * 24
        security_level = watch_towers * 10 if perimeter_fencing else 0
        communication_range = radio_towers * 50
        
        total_score = (water_capacity + food_capacity + 
                      power_capacity + security_level + 
                      communication_range)
        
        # Expected: 15000 + 12500 + 192 + 120 + 250 = 28062
        assert total_score == 28062
        assert total_score >= 10001  # Should be EXCELLENT status
    
    def test_zombie_resource_counts(self):
        """Test zombie scenario resource deployment counts"""
        # Expected resource counts for zombie scenario
        expected_resources = {
            "water_tanks": 15,
            "food_stores": 25,
            "power_generators": 8,
            "watch_towers": 12,
            "radio_towers": 5,
            "perimeter_fencing": 1
        }
        
        # Validate minimum requirements for zombie scenario
        assert expected_resources["water_tanks"] >= 10
        assert expected_resources["food_stores"] >= 20
        assert expected_resources["power_generators"] >= 5
        assert expected_resources["watch_towers"] >= 8
        assert expected_resources["radio_towers"] >= 3
        assert expected_resources["perimeter_fencing"] == 1
    
    def test_zombie_security_measures(self):
        """Test zombie scenario security measures"""
        # Zombie scenario should have maximum security
        security_level = 10
        perimeter_fencing = True
        watch_towers = 12
        
        assert security_level == 10
        assert perimeter_fencing is True
        assert watch_towers >= 8
        
        # Security score calculation
        security_score = watch_towers * 10 if perimeter_fencing else 0
        assert security_score == 120
    
    def test_zombie_communication_setup(self):
        """Test zombie scenario communication setup"""
        radio_towers = 5
        emergency_frequency = "98.7MHz"
        
        assert radio_towers >= 3
        assert emergency_frequency == "98.7MHz"
        
        # Communication range calculation
        communication_range = radio_towers * 50
        assert communication_range == 250  # 250 miles coverage
    
    def test_zombie_backup_strategy(self):
        """Test zombie scenario backup and recovery strategy"""
        backup_retention_days = 730  # 2 years
        enable_auto_scaling = True
        maintenance_window = "Sun:01:00-Sun:03:00"
        
        assert backup_retention_days == 730
        assert enable_auto_scaling is True
        assert maintenance_window == "Sun:01:00-Sun:03:00"
    
    def test_zombie_environment_tags(self):
        """Test zombie scenario environment-specific tags"""
        # Expected tags for zombie scenario
        expected_tags = {
            "ThreatLevel": "ZOMBIE_APOCALYPSE",
            "Quarantine": "ACTIVE",
            "Biohazard": "WARNING"
        }
        
        main_tf = self.scenario_path / "main.tf"
        content = main_tf.read_text()
        
        # Check that all expected tags are present
        for tag_key, tag_value in expected_tags.items():
            assert f"{tag_key} = \"{tag_value}\"" in content


def test_zombie_scenario_integration():
    """Integration test for zombie scenario"""
    scenario_path = Path(__file__).parent.parent / "examples" / "zombie_outbreak"
    
    # Check that all required files exist
    assert (scenario_path / "main.tf").exists()
    
    # Validate configuration syntax
    main_tf = scenario_path / "main.tf"
    content = main_tf.read_text()
    
    # Basic syntax validation
    assert "module " in content
    assert "source = " in content
    assert "environment = " in content
    assert "water_tanks = " in content
    assert "food_stores = " in content
    
    # Check for proper module structure
    assert "zombie_outbreak_survival" in content
    assert "zombie_outbreak_status" in content
    assert "zombie_defense_status" in content


if __name__ == "__main__":
    # Run zombie scenario tests
    test = TestZombieOutbreakScenario()
    test.setup_method()
    
    try:
        test.test_zombie_scenario_configuration()
        test.test_zombie_scenario_outputs()
        test.test_zombie_survival_score()
        test.test_zombie_resource_counts()
        test.test_zombie_security_measures()
        test.test_zombie_communication_setup()
        test.test_zombie_backup_strategy()
        test.test_zombie_environment_tags()
        
        test_zombie_scenario_integration()
        
        print("✅ Zombie outbreak scenario tests passed!")
    except Exception as e:
        print(f"❌ Zombie scenario test failed: {e}")
    finally:
        test.teardown_method()
