import sys
import re

def validate_name(name: str) -> dict:
    """
    Validates a proposed doomsday device name against predefined menacing rules.
    Returns a dictionary with 'approved' status and a list of 'violations'.
    """
    violations = []
    name_lower = name.lower()

    # Rule 1: Length
    if not (10 <= len(name) <= 30):
        violations.append("Length (must be between 10 and 30 characters)")

    # Rule 2: Ominous Keywords
    ominous_keywords = [
        "oblivion", "annihilation", "cataclysm", "ragnarok", "terminus",
        "void", "omega", "destroyer", "harbinger", "apocalypse", "extinction"
    ]
    if not any(re.search(r'\b' + kw + r'\b', name_lower) for kw in ominous_keywords):
        violations.append("Ominous Keywords (missing at least one)")

    # Rule 3: Forbidden Keywords
    forbidden_keywords = [
        "fluffy", "sparkle", "rainbow", "cuddle", "happy", "joy",
        "friendship", "love", "peace", "pony"
    ]
    for kw in forbidden_keywords:
        if re.search(r'\b' + kw + r'\b', name_lower):
            violations.append(f"Forbidden Keywords (contains '{kw}')")
            break # Only report one forbidden keyword for brevity

    # Rule 4: Hard Consonants
    hard_consonants = set('kxqzjgvy')
    found_hard_consonants = set(c for c in name_lower if c in hard_consonants)
    if len(found_hard_consonants) < 2:
        violations.append("Hard Consonants (missing at least two distinct ones)")

    # Rule 5: Approved Suffix
    approved_suffixes = ("inator", "tron", "ex", "prime", "unit", "doom", "strike")
    if not name_lower.endswith(approved_suffixes):
        violations.append("Approved Suffix (must end with one of: inator, tron, ex, prime, unit, doom, strike)")

    return {
        "approved": not bool(violations),
        "violations": violations
    }

def run_cli(args: list) -> int:
    """
    Runs the command-line interface logic for the namer utility.
    Returns 0 for success, 1 for failure.
    """
    if len(args) < 2:
        print("Usage: python src/namer.py \"Your Proposed Doomsday Name\"")
        return 1

    proposed_name = args[1]
    result = validate_name(proposed_name)

    if result["approved"]:
        print(f"Name '{proposed_name}' is Approved for Global Domination!")
        return 0
    else:
        print(f"Name '{proposed_name}' is NOT approved.")
        for violation in result["violations"]:
            print(f"- Rule Violation: {violation}")
        return 1

if __name__ == "__main__":
    sys.exit(run_cli(sys.argv))
