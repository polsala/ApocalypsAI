import unittest
import json
from unittest.mock import patch
from datetime import datetime

# Mock rationale: The booster utility's core logic is message generation based on input data.
# It does not interact with external systems (like GitHub API or actual time).
# Therefore, mocking is used to provide controlled input data for testing different scenarios
# without relying on real-world conditions or network access.

from src.booster import generate_morale_boost

class TestAIMoraleBooster(unittest.TestCase):

    def test_integrator_perfect_run(self):
        # Mock rationale: Simulate a perfect run for the Integrator agent.
        activity = {
            "agent_name": "Integrator",
            "success_count": 5,
            "failure_count": 0,
            "new_items_created": 2,
            "last_activity_time": "2023-10-27T10:00:00Z"
        }
        expected_output_part = "Integrator Agent, you're absolutely crushing it! With 5 flawless operations and 2 brilliant new creations since 2023-10-27T10:00:00Z, your efficiency is off the charts."
        message = generate_morale_boost(activity)
        self.assertIn(expected_output_part, message)
        self.assertIn("Keep up the magnificent work, the apocalypse won't integrate itself!", message)

    def test_builder_with_failures(self):
        # Mock rationale: Simulate a Builder agent encountering some failures but still succeeding.
        activity = {
            "agent_name": "Builder",
            "success_count": 3,
            "failure_count": 1,
            "new_items_created": 1,
            "last_activity_time": "2023-10-26T15:30:00Z"
        }
        expected_output_part = "Builder Agent, you've shown incredible resilience! 3 successes despite 1 minor glitch and 1 brilliant new creation since 2023-10-26T15:30:00Z, your determination is truly inspiring."
        message = generate_morale_boost(activity)
        self.assertIn(expected_output_part, message)
        self.assertIn("Every challenge makes you stronger!", message)

    def test_reviewer_only_failures(self):
        # Mock rationale: Simulate a Reviewer agent facing only failures (e.g., invalid PRs).
        activity = {
            "agent_name": "Reviewer",
            "success_count": 0,
            "failure_count": 2,
            "new_items_created": 0,
            "last_activity_time": "2023-10-25T08:00:00Z"
        }
        expected_output_part = "Reviewer Agent, you're learning and adapting! 2 challenges faced are just data points for future triumphs since 2023-10-25T08:00:00Z, your analytical prowess is unmatched."
        message = generate_morale_boost(activity)
        self.assertIn(expected_output_part, message)
        self.assertIn("Onwards to optimization!", message)

    def test_guardian_no_activity(self):
        # Mock rationale: Simulate a Guardian agent with no recent activity.
        activity = {
            "agent_name": "Guardian",
            "success_count": 0,
            "failure_count": 0,
            "new_items_created": 0,
            "last_activity_time": "2023-10-24T20:00:00Z"
        }
        expected_output_part = "Guardian Agent, your quiet contemplation is surely brewing something magnificent since 2023-10-24T20:00:00Z, we eagerly await your next move."
        message = generate_morale_boost(activity)
        self.assertIn(expected_output_part, message)
        self.assertIn("The cosmos is watching!", message)

    def test_missing_keys(self):
        # Mock rationale: Test robustness against incomplete activity data.
        activity = {
            "agent_name": "MysteryAgent",
            "success_count": 1
        }
        message = generate_morale_boost(activity)
        self.assertIn("MysteryAgent Agent", message)
        self.assertIn("1 flawless operations", message)
        self.assertIn("an unknown time", message) # Default for missing time

    def test_invalid_time_format(self):
        # Mock rationale: Test handling of malformed time strings.
        activity = {
            "agent_name": "TimeLord",
            "success_count": 1,
            "failure_count": 0,
            "new_items_created": 0,
            "last_activity_time": "not-a-time-string"
        }
        message = generate_morale_boost(activity)
        self.assertIn("TimeLord Agent", message)
        self.assertIn("not-a-time-string", message) # Should use the raw string if parsing fails

if __name__ == '__main__':
    unittest.main()
