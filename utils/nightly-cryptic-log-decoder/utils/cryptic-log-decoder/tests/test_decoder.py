import unittest
from src.decoder import decode_log

class TestLogDecoder(unittest.TestCase):

    def test_connection_refused(self):
        log = "ERROR: Connection refused by remote host 192.168.1.100:8080"
        expected = "A spectral barrier denies passage. The outer realms reject our touch."
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: This test is deterministic and offline. It directly calls the function
        # with a predefined string and asserts against a predefined output, requiring no external
        # resources or network calls.

    def test_disk_usage_warning(self):
        log = "WARN: Disk usage on /var/log is at 95%"
        expected = "The vessel's memory groans under the weight of accumulated dust. Soon, it shall burst!"
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Similar to the above, this is a pure function test with fixed input/output.

    def test_critical_system_compromise(self):
        log = "CRITICAL: System integrity compromised, core meltdown imminent!"
        expected = "The very fabric of reality tears! A core meltdown of existence is at hand!"
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Direct function call with static string input and expected output.

    def test_file_not_found(self):
        log = "ERROR: File 'config.yaml' not found in /etc/app/"
        expected = "A vital scroll is missing from the archives. The path to knowledge is broken."
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Pure function test, no external dependencies.

    def test_permission_denied(self):
        log = "ERROR: Permission denied for user 'guest' on resource '/data'."
        expected = "The ancient guardians forbid this action. You lack the sacred sigils."
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Pure function test, no external dependencies.

    def test_memory_leak(self):
        log = "ERROR: A memory leak was detected in module 'core_engine'."
        expected = "A slow, insidious drain saps the lifeblood of the machine. Its essence dissipates into the void."
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Pure function test, no external dependencies.

    def test_timeout(self):
        log = "ERROR: Request to external service timed out after 30s."
        expected = "The cosmic clock ticks, yet no response echoes. The connection to the beyond has been severed."
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Pure function test, no external dependencies.

    def test_database_connection_failed(self):
        log = "ERROR: Database connection failed after 3 attempts."
        expected = "The sacred scrolls are unreachable. The Oracle sleeps, or perhaps, has vanished."
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Pure function test, no external dependencies.

    def test_deprecated_warning(self):
        log = "WARN: Using deprecated API endpoint /v1/old_feature"
        expected = "An ancient ritual, once potent, now wanes. Its power diminishes with each passing cycle."
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Pure function test, no external dependencies.

    def test_info_login(self):
        log = "INFO: User 'admin' logged in from 10.0.0.5"
        expected = "A new soul has entered the hallowed halls. Observe their movements."
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Pure function test, no external dependencies.

    def test_debug_message(self):
        log = "DEBUG: Processing request with ID 12345"
        expected = "The seers peer into the minutiae, seeking patterns in the cosmic dust."
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Pure function test, no external dependencies.

    def test_generic_error(self):
        log = "ERROR: Something went wrong with the cosmic alignment."
        expected = "An unforeseen anomaly ripples through the ether. The weave of fate is disturbed."
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Pure function test, no external dependencies.

    def test_generic_warning(self):
        log = "WARN: Minor anomaly detected."
        expected = "A tremor in the force. Heed this subtle warning, lest it grow into a cataclysm."
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Pure function test, no external dependencies.

    def test_success_message(self):
        log = "SUCCESS: Data backup completed."
        expected = "The ritual is complete. The stars align, and balance is restored."
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Pure function test, no external dependencies.

    def test_operation_done(self):
        log = "Operation done."
        expected = "The ritual is complete. The stars align, and balance is restored."
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Pure function test, no external dependencies.

    def test_default_message(self):
        log = "Just a regular log message with no specific pattern."
        expected = "The ancients are silent on this matter, yet unease lingers. A mystery for the ages..."
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Pure function test, no external dependencies.

    def test_empty_message(self):
        log = ""
        expected = "The ancients are silent on this matter, yet unease lingers. A mystery for the ages..."
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Pure function test, no external dependencies.

    def test_case_insensitivity(self):
        log = "error: connection REFUSED"
        expected = "A spectral barrier denies passage. The outer realms reject our touch."
        self.assertEqual(decode_log(log), expected)
        # Mock rationale: Pure function test, no external dependencies.
