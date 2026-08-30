import subprocess
import sys
import os

def run_script(arg=None):
    cmd = [sys.executable, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "tip_generator.py"))]
    if arg is not None:
        cmd.append(str(arg))
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()

def test_specific_tip():
    # Index 0 should return the first tip
    tip = run_script(0)
    assert tip == "Always keep a spare can‑of‑beans in your bunker."

def test_index_out_of_bounds():
    # Index larger than list returns last tip (clamped)
    tip = run_script(100)
    assert tip == "Plant a cactus; it survives the apocalypse better than you."

def test_random_tip():
    # Run without index; ensure it returns a tip from the list
    tip = run_script()
    # Mock rationale: we cannot predict random, just verify it's one of the known tips
    assert tip in [
        "Always keep a spare can‑of‑beans in your bunker.",
        "Never trust a solar panel that smiles back.",
        "Map your routes with chalk; batteries die faster than you think.",
        "When the wind howls, sing to keep the mutants at bay.",
        "A well‑maintained radio is louder than a screaming crowd.",
        "Store water in copper; it tastes like victory.",
        "Learn to read the stars; GPS is a luxury of the past.",
        "Never leave your flashlight on; darkness is a friend, not a foe.",
        "Barter with jokes; laughter is the most stable currency.",
        "Plant a cactus; it survives the apocalypse better than you."
    ]
