import subprocess
import os


def run_script(env=None):
    env_vars = os.environ.copy()
    if env:
        env_vars.update(env)
    result = subprocess.run(['sh', 'src/main.sh'], env=env_vars, capture_output=True, text=True)
    return result.stdout.strip()


def test_deterministic_index():
    output = run_script({'QUOTE_INDEX': '2'})
    assert output == 'Fortune favors the bold.'


def test_random_output_in_list():
    output = run_script()
    assert output in [
        'To be, or not to be, that is the question.',
        'All that glitters is not gold.',
        'Fortune favors the bold.',
        'Knowledge is power.',
        'Time is money.'
    ]
