import unittest
import string
from src.app import app, generate_password, DEFAULT_LENGTH, MAX_LENGTH

class TestPasswordGenerator(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_default_length(self):
        response = self.client.get('/generate')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('password', data)
        self.assertEqual(len(data['password']), DEFAULT_LENGTH)

    def test_custom_length(self):
        length = 20
        response = self.client.get(f'/generate?length={length}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['password']), length)

    def test_length_bounds(self):
        # Too small
        resp_small = self.client.get('/generate?length=0')
        self.assertEqual(resp_small.status_code, 400)
        # Too large
        resp_large = self.client.get(f'/generate?length={MAX_LENGTH + 1}')
        self.assertEqual(resp_large.status_code, 400)

    def test_character_set(self):
        pwd = generate_password(50)
        allowed = set(string.ascii_letters + string.digits + string.punctuation)
        self.assertTrue(set(pwd).issubset(allowed))

if __name__ == '__main__':
    unittest.main()

