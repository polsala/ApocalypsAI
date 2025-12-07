import unittest
import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import QuantumGarden

class TestQuantumGarden(unittest.TestCase):
    """Test suite for QuantumGarden."""
    
    def test_garden_initialization(self):
        """Test that garden initializes correctly."""
        garden = QuantumGarden(size=10, seed=42)
        self.assertEqual(garden.size, 10)
        self.assertEqual(garden.seed, 42)
        self.assertEqual(len(garden.garden), 10)
        self.assertEqual(len(garden.garden[0]), 10)
        self.assertEqual(garden.generation, 0)
    
    def test_size_clamping(self):
        """Test that garden size is clamped to valid range."""
        garden_small = QuantumGarden(size=3)  # Should be clamped to 5
        garden_large = QuantumGarden(size=100)  # Should be clamped to 50
        
        self.assertEqual(garden_small.size, 5)
        self.assertEqual(garden_large.size, 50)
    
    def test_deterministic_with_seed(self):
        """Test that same seed produces same garden."""
        garden1 = QuantumGarden(size=8, seed=12345)
        garden1.generate_garden()
        
        garden2 = QuantumGarden(size=8, seed=12345)
        garden2.generate_garden()
        
        # Compare garden layouts
        for y in range(garden1.size):
            for x in range(garden1.size):
                self.assertEqual(garden1.garden[y][x], garden2.garden[y][x])
    
    def test_different_seeds_produce_different_gardens(self):
        """Test that different seeds produce different gardens."""
        garden1 = QuantumGarden(size=8, seed=11111)
        garden1.generate_garden()
        
        garden2 = QuantumGarden(size=8, seed=22222)
        garden2.generate_garden()
        
        # Gardens should be different (extremely unlikely to be the same)
        different = False
        for y in range(garden1.size):
            for x in range(garden1.size):
                if garden1.garden[y][x] != garden2.garden[y][x]:
                    different = True
                    break
            if different:
                break
        
        self.assertTrue(different, "Gardens with different seeds should be different")
    
    def test_flower_placement(self):
        """Test that flowers are placed correctly."""
        garden = QuantumGarden(size=5, seed=42)
        garden.generate_garden()
        
        # Check that flowers exist
        self.assertGreater(len(garden.flowers), 0)
        
        # Check that all flowers are within bounds
        for x, y, _, _ in garden.flowers:
            self.assertGreaterEqual(x, 0)
            self.assertLess(x, garden.size)
            self.assertGreaterEqual(y, 0)
            self.assertLess(y, garden.size)
    
    def test_butterfly_placement(self):
        """Test that butterflies are placed correctly."""
        garden = QuantumGarden(size=5, seed=42)
        garden.generate_garden()
        
        # Check that butterflies exist
        self.assertGreater(len(garden.butterflies), 0)
        
        # Check that all butterflies are within bounds
        for x, y, _ in garden.butterflies:
            self.assertGreaterEqual(x, 0)
            self.assertLess(x, garden.size)
            self.assertGreaterEqual(y, 0)
            self.assertLess(y, garden.size)
    
    def test_entanglement_creation(self):
        """Test that entanglement pairs are created."""
        garden = QuantumGarden(size=10, seed=42)
        garden.generate_garden()
        
        # Should have some entangled pairs if there are enough butterflies
        if len(garden.butterflies) >= 2:
            self.assertGreater(len(garden.entangled_pairs), 0)
        
        # Check that entangled pairs reference valid butterflies
        for pair in garden.entangled_pairs:
            self.assertEqual(len(pair), 2)
            self.assertGreaterEqual(pair[0], 0)
            self.assertLess(pair[0], len(garden.butterflies))
            self.assertGreaterEqual(pair[1], 0)
            self.assertLess(pair[1], len(garden.butterflies))
            self.assertNotEqual(pair[0], pair[1])  # Should be different butterflies
    
    def test_growth_step_increments_generation(self):
        """Test that growth steps increment generation counter."""
        garden = QuantumGarden(size=5, seed=42)
        garden.generate_garden()
        
        initial_generation = garden.generation
        garden.grow_step()
        
        self.assertEqual(garden.generation, initial_generation + 1)
    
    def test_quantum_tunnel(self):
        """Test quantum tunneling functionality."""
        garden = QuantumGarden(size=5, seed=42)
        
        # Test tunneling from center
        x, y = 2, 2
        new_x, new_y = garden._quantum_tunnel(x, y)
        
        # Should be within reasonable range
        self.assertGreaterEqual(new_x, 0)
        self.assertLess(new_x, garden.size)
        self.assertGreaterEqual(new_y, 0)
        self.assertLess(new_y, garden.size)
        
        # Should be close to original (within 2 cells)
        self.assertLessEqual(abs(new_x - x), 2)
        self.assertLessEqual(abs(new_y - y), 2)
    
    def test_observe_garden_collapses_superposition(self):
        """Test that observation collapses quantum superposition."""
        garden = QuantumGarden(size=5, seed=42)
        garden.generate_garden()
        
        # Manually create a flower in superposition
        if garden.flowers:
            x, y, flower_type, _ = garden.flowers[0]
            garden.flowers[0] = (x, y, flower_type, True)  # Force superposition
            
            initial_type = garden.garden[y][x]
            garden._observe_garden()
            
            # After observation, superposition should be collapsed
            _, _, _, superposition = garden.flowers[0]
            self.assertFalse(superposition)
    
    def test_render_output(self):
        """Test that render produces valid output."""
        garden = QuantumGarden(size=5, seed=42)
        garden.generate_garden()
        
        output = garden.render()
        
        # Check that output contains expected elements
        self.assertIn("Quantum Garden", output)
        self.assertIn(f"Gen: {garden.generation}", output)
        self.assertIn("=" * (garden.size + 4), output)
        self.assertIn("|", output)
    
    def test_quantum_random_distribution(self):
        """Test that quantum random produces values in expected range."""
        garden = QuantumGarden(seed=42)
        
        values = []
        for _ in range(100):
            values.append(garden._quantum_random(0.0, 1.0))
        
        # All values should be in range
        for val in values:
            self.assertGreaterEqual(val, 0.0)
            self.assertLessEqual(val, 1.0)
    
    def test_empty_garden_render(self):
        """Test rendering an empty garden."""
        garden = QuantumGarden(size=3, seed=42)
        # Don't call generate_garden() to keep it empty
        
        output = garden.render()
        
        # Should still produce valid output
        self.assertIn("Quantum Garden", output)
        self.assertIn("Gen: 0", output)
    
    def test_large_garden(self):
        """Test that large gardens work correctly."""
        garden = QuantumGarden(size=50, seed=42)
        garden.generate_garden()
        
        # Should handle large size without errors
        self.assertEqual(len(garden.garden), 50)
        self.assertEqual(len(garden.garden[0]), 50)
        
        # Should be able to grow
        garden.grow_step()
        self.assertEqual(garden.generation, 1)
    
    def test_multiple_growth_cycles(self):
        """Test multiple growth cycles."""
        garden = QuantumGarden(size=8, seed=42)
        garden.generate_garden()
        
        initial_flowers = len(garden.flowers)
        initial_butterflies = len(garden.butterflies)
        
        # Run several growth cycles
        for _ in range(5):
            garden.grow_step()
        
        # Should have more flowers (they spread)
        self.assertGreaterEqual(len(garden.flowers), initial_flowers)
        
        # Generation should have incremented
        self.assertEqual(garden.generation, 5)


def run_tests():
    """Run all tests with a simple test runner."""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestQuantumGarden)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
