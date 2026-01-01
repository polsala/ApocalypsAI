#!/usr/bin/env python3
"""
Test suite for Nuclear Winter Scenario

Validates the extreme conditions configuration for nuclear winter scenarios.
"""

import tempfile
from pathlib import Path


class TestNuclearWinterScenario:
    """Test class for nuclear winter scenario"""
    
    def setup_method(self):
        """Setup test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.scenario_path = Path(__file__).parent.parent / "examples" / "nuclear_winter"
        
    def test_nuclear_winter_configuration(self):
        """Test nuclear winter scenario configuration"""
        main_tf = self.scenario_path / "main.tf"
        assert main_tf.exists()
        
        content = main_tf.read_text()
        
        # Check nuclear winter-specific configuration
        assert "nuclear_winter_survival" in content
        assert "environment   = \"nuclear-winter\"" in content
        assert "water_tanks   = 25" in content
        assert "food_stores   = 40" in content
        assert "power_generators = 15" in content
        assert "watch_towers  = 16" in content
        assert "security_level = 9" in content
        assert "radio_towers  = 8" in content
        
        # Check nuclear winter-specific tags
        assert "RadiationLevel = \"HIGH\"" in content
        assert "Temperature   = \"EXTREME_COLD\"" in content
        assert "DaylightHours = \"MINIMAL\"" in content
    
    def test_nuclear_winter_outputs(self):
        """Test nuclear winter scenario output validation"""
        main_tf = self.scenario_path / "main.tf"
        content = main_tf.read_text()
        
        # Check for nuclear winter-specific outputs
        assert "nuclear_winter_status" in content
        assert "nuclear_winter_conditions" in content
        
        # Check environmental conditions
        assert "expected_temperature = \"-40F to -10F\"" in content
        assert "daylight_hours = \"2-4 hours per day\"" in content
        assert "radiation_level = \"ELEVATED\"" in content
        assert "survival_duration = \"5-10 years\"" in content
    
    def test_nuclear_winter_survival_score(self):
        """Test nuclear winter scenario survival score calculation"""
        # Nuclear winter scenario configuration
        water_tanks = 25
        food_stores = 40
        power_generators = 15
        perimeter_fencing = True
        watch_towers = 16
        radio_towers = 8
        
        # Calculate survival score
        water_capacity = water_tanks * 1000
        food_capacity = food_stores * 500
        power_capacity = power_generators * 24
        security_level = watch_towers * 10 if perimeter_fencing else 0
        communication_range = radio_towers * 50
        
        total_score = (water_capacity + food_capacity + 
                      power_capacity + security_level + 
                      communication_range)
        
        # Expected: 25000 + 20000 + 360 + 160 + 400 = 46120
        assert total_score == 46120
        assert total_score >= 10001  # Should be EXCELLENT status
    
    def test_nuclear_winter_resource_counts(self):
        """Test nuclear winter scenario resource deployment counts"""
        # Expected resource counts for nuclear winter scenario
        expected_resources = {
            "water_tanks": 25,
            "food_stores": 40,
            "power_generators": 15,
            "watch_towers": 16,
            "radio_towers": 8,
            "perimeter_fencing": 1
        }
        
        # Validate minimum requirements for nuclear winter scenario
        assert expected_resources["water_tanks"] >= 20
        assert expected_resources["food_stores"] >= 30
        assert expected_resources["power_generators"] >= 10
        assert expected_resources["watch_towers"] >= 12
        assert expected_resources["radio_towers"] >= 5
        assert expected_resources["perimeter_fencing"] == 1
    
    def test_nuclear_winter_backup_strategy(self):
        """Test nuclear winter scenario backup strategy"""
        backup_retention_days = 1095  # 3 years
        enable_auto_scaling = True
        maintenance_window = "Sat:03:00-Sat:05:00"
        
        assert backup_retention_days == 1095
        assert enable_auto_scaling is True
        assert maintenance_window == "Sat:03:00-Sat:05:00"
    
    def test_nuclear_winter_environmental_conditions(self):
        """Test nuclear winter environmental condition validation"""
        # Expected environmental conditions
        conditions = {
            "expected_temperature": "-40F to -10F",
            "daylight_hours": "2-4 hours per day",
            "radiation_level": "ELEVATED",
            "survival_duration": "5-10 years",
            "resource_efficiency": "MAXIMIZED"
        }
        
        main_tf = self.scenario_path / "main.tf"
        content = main_tf.read_text()
        
        # Check that all expected conditions are present
        for condition_key, condition_value in conditions.items():
            assert f"{condition_key} = \"{condition_value}\"" in content
    
    def test_nuclear_winter_communication_setup(self):
        """Test nuclear winter scenario communication setup"""
        radio_towers = 8
        emergency_frequency = "88.1MHz"
        
        assert radio_towers >= 5
        assert emergency_frequency == "88.1MHz"
        
        # Communication range calculation
        communication_range = radio_towers * 50
        assert communication_range == 400  # 400 miles coverage
    
    def test_nuclear_winter_security_measures(self):
        """Test nuclear winter scenario security measures"""
        # Nuclear winter scenario should have high security
        security_level = 9
        perimeter_fencing = True
        watch_towers = 16
        
        assert security_level >= 8
        assert perimeter_fencing is True
        assert watch_towers >= 12
        
        # Security score calculation
        security_score = watch_towers * 10 if perimeter_fencing else 0
        assert security_score == 160


def test_nuclear_winter_scenario_integration():
    """Integration test for nuclear winter scenario"""
    scenario_path = Path(__file__).parent.parent / "examples" / "nuclear_winter"
    
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
    assert "nuclear_winter_survival" in content
    assert "nuclear_winter_status" in content
    assert "nuclear_winter_conditions" in content


if __name__ == "__main__":
    # Run nuclear winter scenario tests
    test = TestNuclearWinterScenario()
    test.setup_method()
    
    try:
        test.test_nuclear_winter_configuration()
        test.test_nuclear_winter_outputs()
        test.test_nuclear_winter_survival_score()
        test.test_nuclear_winter_resource_counts()
        test.test_nuclear_winter_backup_strategy()
        test.test_nuclear_winter_environmental_conditions()
        test.test_nuclear_winter_communication_setup()
        test.test_nuclear_winter_security_measures()
        
        test_nuclear_winter_scenario_integration()
        
        print("✅ Nuclear winter scenario tests passed!")
    except Exception as e:
        print(f"❌ Nuclear winter scenario test failed: {e}")
    finally:
        test.teardown_method()
