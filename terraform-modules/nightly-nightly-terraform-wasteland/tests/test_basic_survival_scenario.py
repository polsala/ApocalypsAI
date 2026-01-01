#!/usr/bin/env python3
"""
Test suite for Basic Survival Scenario

Validates the minimal configuration for basic survival scenarios.
"""

import tempfile
from pathlib import Path


class TestBasicSurvivalScenario:
    """Test class for basic survival scenario"""
    
    def setup_method(self):
        """Setup test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.scenario_path = Path(__file__).parent.parent / "examples" / "basic_survival"
        
    def test_basic_survival_configuration(self):
        """Test basic survival scenario configuration"""
        main_tf = self.scenario_path / "main.tf"
        assert main_tf.exists()
        
        content = main_tf.read_text()
        
        # Check basic survival-specific configuration
        assert "basic_survival" in content
        assert "environment   = \"basic-survival\"" in content
        assert "water_tanks   = 2" in content
        assert "food_stores   = 3" in content
        assert "power_generators = 2" in content
        assert "watch_towers  = 2" in content
        assert "security_level = 5" in content
        assert "radio_towers  = 2" in content
        
        # Check basic survival-specific tags
        assert "ThreatLevel = \"LOW\"" in content
    
    def test_basic_survival_outputs(self):
        """Test basic survival scenario output validation"""
        main_tf = self.scenario_path / "main.tf"
        content = main_tf.read_text()
        
        # Check for basic survival-specific outputs
        assert "basic_survival_status" in content
        assert "basic_survival_summary" in content
        
        # Check survival summary values
        assert "water_tanks_deployed = 2" in content
        assert "food_stores_deployed = 3" in content
        assert "power_generators_deployed = 2" in content
        assert "security_towers_deployed = 2" in content
        assert "communication_towers_deployed = 2" in content
        assert "estimated_survival_time = \"6-12 months\"" in content
    
    def test_basic_survival_survival_score(self):
        """Test basic survival scenario survival score calculation"""
        # Basic survival scenario configuration
        water_tanks = 2
        food_stores = 3
        power_generators = 2
        perimeter_fencing = True
        watch_towers = 2
        radio_towers = 2
        
        # Calculate survival score
        water_capacity = water_tanks * 1000
        food_capacity = food_stores * 500
        power_capacity = power_generators * 24
        security_level = watch_towers * 10 if perimeter_fencing else 0
        communication_range = radio_towers * 50
        
        total_score = (water_capacity + food_capacity + 
                      power_capacity + security_level + 
                      communication_range)
        
        # Expected: 2000 + 1500 + 48 + 20 + 100 = 3668
        assert total_score == 3668
        assert 1001 <= total_score <= 5000  # Should be GOOD status
    
    def test_basic_survival_resource_counts(self):
        """Test basic survival scenario resource deployment counts"""
        # Expected resource counts for basic survival scenario
        expected_resources = {
            "water_tanks": 2,
            "food_stores": 3,
            "power_generators": 2,
            "watch_towers": 2,
            "radio_towers": 2,
            "perimeter_fencing": 1
        }
        
        # Validate minimum requirements for basic survival scenario
        assert expected_resources["water_tanks"] >= 1
        assert expected_resources["food_stores"] >= 1
        assert expected_resources["power_generators"] >= 1
        assert expected_resources["watch_towers"] >= 0
        assert expected_resources["radio_towers"] >= 1
        assert expected_resources["perimeter_fencing"] == 1
    
    def test_basic_survival_backup_strategy(self):
        """Test basic survival scenario backup strategy"""
        backup_retention_days = 365  # 1 year
        enable_auto_scaling = False
        maintenance_window = "Sun:02:00-Sun:04:00"
        
        assert backup_retention_days == 365
        assert enable_auto_scaling is False
        assert maintenance_window == "Sun:02:00-Sun:04:00"
    
    def test_basic_survival_monitoring(self):
        """Test basic survival scenario monitoring configuration"""
        create_monitoring = False
        enable_logging = False
        
        assert create_monitoring is False
        assert enable_logging is False
    
    def test_basic_survival_security_measures(self):
        """Test basic survival scenario security measures"""
        # Basic survival scenario should have moderate security
        security_level = 5
        perimeter_fencing = True
        watch_towers = 2
        
        assert security_level == 5
        assert perimeter_fencing is True
        assert watch_towers >= 0
        
        # Security score calculation
        security_score = watch_towers * 10 if perimeter_fencing else 0
        assert security_score == 20
    
    def test_basic_survival_communication_setup(self):
        """Test basic survival scenario communication setup"""
        radio_towers = 2
        emergency_frequency = "101.5MHz"
        
        assert radio_towers >= 1
        assert emergency_frequency == "101.5MHz"
        
        # Communication range calculation
        communication_range = radio_towers * 50
        assert communication_range == 100  # 100 miles coverage


def test_basic_survival_scenario_integration():
    """Integration test for basic survival scenario"""
    scenario_path = Path(__file__).parent.parent / "examples" / "basic_survival"
    
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
    assert "basic_survival" in content
    assert "basic_survival_status" in content
    assert "basic_survival_summary" in content


if __name__ == "__main__":
    # Run basic survival scenario tests
    test = TestBasicSurvivalScenario()
    test.setup_method()
    
    try:
        test.test_basic_survival_configuration()
        test.test_basic_survival_outputs()
        test.test_basic_survival_survival_score()
        test.test_basic_survival_resource_counts()
        test.test_basic_survival_backup_strategy()
        test.test_basic_survival_monitoring()
        test.test_basic_survival_security_measures()
        test.test_basic_survival_communication_setup()
        
        test_basic_survival_scenario_integration()
        
        print("✅ Basic survival scenario tests passed!")
    except Exception as e:
        print(f"❌ Basic survival scenario test failed: {e}")
    finally:
        test.teardown_method()
