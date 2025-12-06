# Doomsday Device Naming Convention Enforcer

## Overview
Welcome, aspiring architects of global despair! This utility, the `Doomsday Device Naming Convention Enforcer`, is designed to ensure that your world-ending contraptions are bestowed with names befitting their destructive grandeur. No more 'Fluffy Destroyer 3000' or 'Happy Annihilator'! We enforce strict, menacing guidelines to maximize fear, despair, and overall apocalyptic brand consistency.

## How it Works
The `namer.py` script takes a proposed device name as input and validates it against a set of predefined rules. If the name passes all checks, it's deemed 'Approved for Global Domination'. Otherwise, it provides feedback on which rules were violated.

## Naming Rules
To be an officially sanctioned Doomsday Device Name, your proposal must adhere to the following:

1.  **Length**: Must be between 10 and 30 characters long (inclusive).
2.  **Ominous Keywords**: Must contain at least one of these words (case-insensitive): `Oblivion`, `Annihilation`, `Cataclysm`, `Ragnarok`, `Terminus`, `Void`, `Omega`, `Destroyer`, `Harbinger`, `Apocalypse`, `Extinction`.
3.  **Forbidden Keywords**: Must NOT contain any of these words (case-insensitive): `Fluffy`, `Sparkle`, `Rainbow`, `Cuddle`, `Happy`, `Joy`, `Friendship`, `Love`, `Peace`, `Pony`.
4.  **Hard Consonants**: Must contain at least two distinct 'hard' consonants (case-insensitive): `K`, `X`, `Z`, `Q`, `G`, `J`, `V`.
5.  **Approved Suffix**: Must end with one of these suffixes (case-insensitive): `inator`, `tron`, `ex`, `prime`, `unit`, `doom`, `strike`.

## Usage
```bash
python src/namer.py "Your Proposed Doomsday Name"
```

### Example Approved Name:
```bash
python src/namer.py "The Omega Annihilation-X Prime"
# Output: Name 'The Omega Annihilation-X Prime' is Approved for Global Domination!
```

### Example Rejected Name:
```bash
python src/namer.py "Fluffy Sparkletron"
# Output: Name 'Fluffy Sparkletron' is NOT approved.
# - Rule Violation: Length (must be between 10 and 30 characters)
# - Rule Violation: Ominous Keywords (missing at least one)
# - Rule Violation: Forbidden Keywords (contains 'fluffy')
# - Rule Violation: Hard Consonants (missing at least two distinct ones)
```

## Development
To run tests:
```bash
python -m unittest tests/test_namer.py
```
