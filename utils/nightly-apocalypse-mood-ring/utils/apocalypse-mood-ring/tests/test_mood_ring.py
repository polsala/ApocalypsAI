import unittest
import sys
from unittest.mock import patch

# Mock rationale: We need to ensure the test environment is clean and isolated.
# By modifying sys.path, we allow the test to import the module under test
# without relying on it being installed or in the global Python path.
# This makes the test self-contained and deterministic.
sys.path.insert(0, 'utils/apocalypse-mood-ring/src')
from mood_ring import get_apocalypse_mood
sys.path.pop(0)

class TestApocalypseMoodRing(unittest.TestCase):

    def test_impending_doom_mood(self):
        self.assertEqual(get_apocalypse_mood("Critical system failure detected. The end is nigh!"), ("Impending Doom", "Red"))
        self.assertEqual(get_apocalypse_mood("Apocalypse is upon us, total collapse."), ("Impending Doom", "Red"))
        self.assertEqual(get_apocalypse_mood("FATAL ERROR: Meltdown imminent."), ("Impending Doom", "Red"))
        self.assertEqual(get_apocalypse_mood("Despair and ruin everywhere."), ("Impending Doom", "Red"))
        self.assertEqual(get_apocalypse_mood("This is a critical disaster."), ("Impending Doom", "Red"))

    def test_slightly_uneasy_mood(self):
        self.assertEqual(get_apocalypse_mood("Minor network instability, monitoring situation."), ("Slightly Uneasy", "Orange"))
        self.assertEqual(get_apocalypse_mood("There's a bug in production, needs attention."), ("Slightly Uneasy", "Orange"))
        self.assertEqual(get_apocalypse_mood("Alert: Potential security risk identified."), ("Slightly Uneasy", "Orange"))
        self.assertEqual(get_apocalypse_mood("Uncertain future for this feature."), ("Slightly Uneasy", "Orange"))
        self.assertEqual(get_apocalypse_mood("Encountered a problem during deployment."), ("Slightly Uneasy", "Orange"))

    def test_post_apocalyptic_chill_mood(self):
        self.assertEqual(get_apocalypse_mood("After the great reboot, we're rebuilding stronger than ever! Feeling optimistic."), ("Post-Apocalyptic Chill", "Blue"))
        self.assertEqual(get_apocalypse_mood("Hope for a new beginning with this refactor."), ("Post-Apocalyptic Chill", "Blue"))
        self.assertEqual(get_apocalypse_mood("Finding peace in the recovery process."), ("Post-Apocalyptic Chill", "Blue"))
        self.assertEqual(get_apocalypse_mood("Thriving in the new environment."), ("Post-Apocalyptic Chill", "Blue"))
        self.assertEqual(get_apocalypse_mood("Serene growth after the storm."), ("Post-Apocalyptic Chill", "Blue"))

    def test_business_as_usual_mood(self):
        self.assertEqual(get_apocalypse_mood("Daily backup completed successfully. All systems nominal."), ("Business as Usual", "Green"))
        self.assertEqual(get_apocalypse_mood("Fixed a minor typo in the documentation."), ("Business as Usual", "Green"))
        self.assertEqual(get_apocalypse_mood("Update dependencies to latest versions."), ("Business as Usual", "Green"))
        self.assertEqual(get_apocalypse_mood("Working on a new feature, progress is good."), ("Business as Usual", "Green"))
        self.assertEqual(get_apocalypse_mood("This is a completely neutral statement."), ("Business as Usual", "Green")) # Default case
        self.assertEqual(get_apocalypse_mood("System is fully operational."), ("Business as Usual", "Green"))

    def test_mysterious_void_mood(self):
        self.assertEqual(get_apocalypse_mood(""), ("Mysterious Void", "Purple"))
        self.assertEqual(get_apocalypse_mood("   \n\t "), ("Mysterious Void", "Purple"))

    def test_case_insensitivity(self):
        self.assertEqual(get_apocalypse_mood("APOCALYPSE NOW!"), ("Impending Doom", "Red"))
        self.assertEqual(get_apocalypse_mood("monitor the situation"), ("Slightly Uneasy", "Orange"))
        self.assertEqual(get_apocalypse_mood("Rebuild the system"), ("Post-Apocalyptic Chill", "Blue"))
        self.assertEqual(get_apocalypse_mood("Success is ours"), ("Business as Usual", "Green"))

    def test_priority_order(self):
        # A text containing keywords for multiple moods should prioritize the most severe
        self.assertEqual(get_apocalypse_mood("We fixed a bug, but the system is still unstable and facing imminent collapse."), ("Impending Doom", "Red"))
        self.assertEqual(get_apocalypse_mood("Progress is good, but there's a warning about potential instability."), ("Slightly Uneasy", "Orange"))
        self.assertEqual(get_apocalypse_mood("We are rebuilding, but there was a minor issue."), ("Slightly Uneasy", "Orange"))
        self.assertEqual(get_apocalypse_mood("Daily task completed, feeling optimistic about the future."), ("Post-Apocalyptic Chill", "Blue"))

if __name__ == '__main__':
    unittest.main()
