'''Tests for the deterministic haiku generator.
\nAll tests run offline and use only the standard library.\n'''\n\nimport unittest\n\nfrom src.haiku_generator import generate_haiku\n\n\nclass TestHaikuGenerator(unittest.TestCase):\n    def test_known_seed(self):\n        # Mock rationale: using a fixed seed ensures the output is deterministic.\n        seed = 42\n        expected = (\n            "Silent moonlight glows\n"
            "Whispers echo through the pine forest\n"
            "Crimson leaves fall"
        )\n        self.assertEqual(generate_haiku(seed), expected)\n\n    def test_different_seeds_produce_different_haikus(self):\n        haiku_a = generate_haiku(1)\n        haiku_b = generate_haiku(2)\n        self.assertNotEqual(haiku_a, haiku_b)\n\n\nif __name__ == "__main__":\n    unittest.main()\n
