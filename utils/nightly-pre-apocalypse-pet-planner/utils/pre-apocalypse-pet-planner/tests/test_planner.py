import unittest
from unittest.mock import patch
import io
from src.planner import generate_checklist

class TestPetPlanner(unittest.TestCase):

    def test_dog_checklist(self):
        checklist = generate_checklist("Fido", "dog")
        self.assertIn("# Apocalypse Preparedness Checklist for Fido (Dog)", checklist)
        self.assertIn("2 weeks supply of Fido's favorite kibble/wet food", checklist)
        self.assertIn("Leash/Harness", checklist)
        self.assertIn("Waste bags and a designated potty area plan", checklist)
        self.assertIn("Training: Ensure basic commands are reinforced", checklist)
        self.assertNotIn("Litter box", checklist)

    def test_cat_checklist(self):
        checklist = generate_checklist("Whiskers", "cat")
        self.assertIn("# Apocalypse Preparedness Checklist for Whiskers (Cat)", checklist)
        self.assertIn("2 weeks supply of Whiskers' favorite kibble/wet food", checklist)
        self.assertIn("Litter box, litter, scoop, and waste bags", checklist)
        self.assertIn("Training: Ensure basic commands are reinforced", checklist)
        self.assertNotIn("Waste bags and a designated potty area plan", checklist)

    def test_bird_checklist(self):
        checklist = generate_checklist("Chirpy", "bird")
        self.assertIn("# Apocalypse Preparedness Checklist for Chirpy (Bird)", checklist)
        self.assertIn("Habitat Essentials: Appropriate bedding, heating/lighting elements", checklist)
        self.assertNotIn("Leash/Harness", checklist)
        self.assertNotIn("Litter box", checklist)
        self.assertNotIn("Training", checklist)

    def test_reptile_checklist(self):
        checklist = generate_checklist("Scaly", "reptile")
        self.assertIn("# Apocalypse Preparedness Checklist for Scaly (Reptile)", checklist)
        self.assertIn("Habitat Essentials: Appropriate bedding, heating/lighting elements", checklist)
        self.assertNotIn("Leash/Harness", checklist)
        self.assertNotIn("Litter box", checklist)
        self.assertNotIn("Training", checklist)

    def test_fish_checklist(self):
        checklist = generate_checklist("Bubbles", "fish")
        self.assertIn("# Apocalypse Preparedness Checklist for Bubbles (Fish)", checklist)
        self.assertIn("Habitat Essentials: Appropriate bedding, heating/lighting elements", checklist)
        self.assertNotIn("Leash/Harness", checklist)
        self.assertNotIn("Litter box", checklist)
        self.assertNotIn("Training", checklist)

    def test_special_needs(self):
        checklist = generate_checklist("Whiskers", "cat", special_needs="Insulin for diabetes")
        self.assertIn("Medication: Insulin for diabetes (2-week supply) and any necessary administration tools.", checklist)
        self.assertIn("Litter box, litter, scoop, and waste bags", checklist)

    def test_no_special_needs(self):
        checklist = generate_checklist("Fido", "dog")
        self.assertNotIn("Medication:", checklist)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_functionality(self, mock_stdout):
        # Mock rationale: Capture stdout to verify the script's print output without affecting actual console.
        with patch('argparse.ArgumentParser.parse_args') as mock_args:
            mock_args.return_value.name = "Buddy"
            mock_args.return_value.type = "dog"
            mock_args.return_value.special_needs = None
            
            # Import and run the main part of the script
            import src.planner as planner_module
            # Reload the module to ensure __name__ == "__main__" is hit
            import importlib
            importlib.reload(planner_module)

            output = mock_stdout.getvalue()
            self.assertIn("# Apocalypse Preparedness Checklist for Buddy (Dog)", output)
            self.assertIn("2 weeks supply of Buddy's favorite kibble/wet food", output)
            self.assertNotIn("Medication:", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_functionality_with_special_needs(self, mock_stdout):
        # Mock rationale: Capture stdout to verify the script's print output without affecting actual console.
        with patch('argparse.ArgumentParser.parse_args') as mock_args:
            mock_args.return_value.name = "Mittens"
            mock_args.return_value.type = "cat"
            mock_args.return_value.special_needs = "daily eye drops"
            
            import src.planner as planner_module
            import importlib
            importlib.reload(planner_module)

            output = mock_stdout.getvalue()
            self.assertIn("# Apocalypse Preparedness Checklist for Mittens (Cat)", output)
            self.assertIn("Medication: daily eye drops (2-week supply)", output)
            self.assertIn("Litter box, litter, scoop, and waste bags", output)

if __name__ == '__main__':
    unittest.main()
