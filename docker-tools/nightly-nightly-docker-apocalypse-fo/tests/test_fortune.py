import subprocess, os, pathlib

def run_fortune(index):
    env = os.environ.copy()
    env["FORTUNE_INDEX"] = str(index)
    result = subprocess.run(
        ["bash", "src/fortune.sh"],
        cwd=pathlib.Path(__file__).parents[1],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()

def test_fortune_first():
    assert run_fortune(1) == "When the sky cracks, remember to bring an umbrella."

def test_fortune_third():
    assert run_fortune(3) == "Your coffee will survive the fallout."
