import unittest
import tempfile
import pathlib
from src import size_estimator

class TestSizeEstimator(unittest.TestCase):
    def test_basic_estimate(self):
        dockerfile_content = (
            "FROM python:3.11-slim\n"
            "COPY . /app\n"
            "RUN pip install -r requirements.txt\n"
            "ADD src/ /src/\n"
        )
        with tempfile.NamedTemporaryFile('w', delete=False) as tf:
            tf.write(dockerfile_content)
            tf_path = tf.name
        # Expected: base 120 + COPY 1 + RUN 5 + ADD 1 = 127 MB
        expected = 127
        result = size_estimator.estimate(tf_path)
        self.assertEqual(result, expected)
        pathlib.Path(tf_path).unlink()

    def test_unknown_base(self):
        dockerfile_content = "FROM unknown:latest\nRUN echo hi\n"
        with tempfile.NamedTemporaryFile('w', delete=False) as tf:
            tf.write(dockerfile_content)
            tf_path = tf.name
        # Default base 100 + RUN 5 = 105 MB
        self.assertEqual(size_estimator.estimate(tf_path), 105)
        pathlib.Path(tf_path).unlink()

if __name__ == "__main__":
    unittest.main()
