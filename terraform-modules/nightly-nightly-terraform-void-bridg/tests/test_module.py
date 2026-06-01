import unittest
import pathlib
import re

class TestVoidBridgeModule(unittest.TestCase):
    def setUp(self):
        # Load file contents once for all tests
        self.base_path = pathlib.Path(__file__).parents[1] / "src"
        self.main_tf = (self.base_path / "main.tf").read_text()
        self.variables_tf = (self.base_path / "variables.tf").read_text()
        self.outputs_tf = (self.base_path / "outputs.tf").read_text()

    def test_security_group_resource_exists(self):
        """Ensure the aws_security_group resource is defined with the correct name attribute."""
        pattern = r'resource\s+"aws_security_group"\s+"void_bridge"\s*{[^}]*name\s*=\s*var\.name'
        self.assertRegex(self.main_tf, pattern, "aws_security_group resource missing or mis‑configured")

    def test_ingress_rule_uses_count(self):
        """Check that the ingress rule uses count based on var.rule_count and generates random CIDR blocks."""
        self.assertIn('count             = var.rule_count', self.main_tf)
        self.assertIn('cidr_blocks       = [cidrsubnet("10.0.0.0/8", 8, count.index)]', self.main_tf)

    def test_default_rule_count_is_one(self):
        """Validate that the default for rule_count is 1 in variables.tf."""
        match = re.search(r'variable\s+"rule_count"[^{]*{[^}]*default\s*=\s*(\d+)', self.variables_tf, re.DOTALL)
        self.assertIsNotNone(match, "rule_count variable missing default")
        self.assertEqual(int(match.group(1)), 1, "Default rule_count should be 1")

    def test_output_defined(self):
        """Confirm that the module outputs the security_group_id."""
        self.assertIn('output "security_group_id"', self.outputs_tf)
        self.assertIn('value       = aws_security_group.void_bridge.id', self.outputs_tf)

if __name__ == "__main__":
    unittest.main()
