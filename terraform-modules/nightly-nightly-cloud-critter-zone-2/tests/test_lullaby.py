import unittest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src/lambda directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/lambda')))

import lullaby # type: ignore # noqa: E402

class TestLullabyLambda(unittest.TestCase):
    @patch('builtins.print')
    def test_lullaby_handler(self, mock_print):
        event = {}
        context = MagicMock()
        
        result = lullaby.handler(event, context)
        
        self.assertEqual(result, {
            'statusCode': 200,
            'body': json.dumps('Critter tucked in for the night!')
        })
        mock_print.assert_called_with("Critter tucked in for the night!")

    # Mock rationale: The 'print' function is mocked to capture its output
    # without affecting the console during testing. The 'context' object is
    # mocked using MagicMock as it's an AWS Lambda runtime object not available
    # in a local test environment and its specific methods are not critical
    # for this simple handler's logic. This ensures the test is deterministic
    # and offline.

if __name__ == '__main__':
    unittest.main()
