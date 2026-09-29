import unittest
import tempfile
import os
from src.analyze import estimate_size

class TestDockerfileSizeEstimator(unittest.TestCase):
    def test_basic_estimation(self):
        dockerfile_content = """
        FROM python:3.11-slim
        COPY requirements.txt .
        RUN pip install -r requirements.txt
        COPY . .
        RUN python -m compileall .
        """
        with tempfile.NamedTemporaryFile('w', delete=False) as tf:
            tf.write(dockerfile_content)
            tf_path = tf.name
        try:
            # Expected: base 30 + 2 RUN *50 =100 + 2 COPY*5 =10 => 140 MB
            self.assertEqual(estimate_size(tf_path), 140)
        finally:
            os.remove(tf_path)

    def test_unknown_base_image_uses_default(self):
        dockerfile_content = """
        FROM unknown/image:latest
        RUN echo hello
        """
        with tempfile.NamedTemporaryFile('w', delete=False) as tf:
            tf.write(dockerfile_content)
            tf_path = tf.name
        try:
            # Expected: default base 20 + 1 RUN*50 =70 MB
            self.assertEqual(estimate_size(tf_path), 70)
        finally:
            os.remove(tf_path)

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            estimate_size("nonexistent/Dockerfile")

if __name__ == "__main__":
    unittest.main()
