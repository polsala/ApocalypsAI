import subprocess
import re
import os
import sys

SCRIPT = os.path.join(\"src\", \"main.sh\")

def run_script(args):
    result = subprocess.run(
        [\"/usr/bin/env\", \"bash\", SCRIPT] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )
    return result.stdout.strip()

def test_deterministic_output():
    output = run_script([\"--seed\", \"42\"])
    expected = \"🌟 Tip: Learn basic first-aid skills. 🩹\"
    assert output == expected

def test_list_tips():
    output = run_script([\"-l\"])
    # Should contain all tips
    for tip in [
        \"Carry a multi-tool for unexpected repairs.\",
        \"Keep a small stash of high-energy snacks.\",
        \"Learn basic first-aid skills.\",
        \"Maintain a clean water source.\",
        \"Practice silent communication.\"
    ]:
        assert tip in output

def test_random_output_pattern():
    output = run_script([])
    # Pattern: \"🌟 Tip: <text> <emoji>\"
    pattern = r\"^🌟 Tip: .+ [\\\\w\\\\W]$\"
    assert re.match(pattern, output)

