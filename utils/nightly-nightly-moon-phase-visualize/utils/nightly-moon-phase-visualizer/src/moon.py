import sys
import datetime
from typing import Tuple

# ---------------------------------------------------------------------------
# Moon phase calculation (based on a simple lunation algorithm)
# ---------------------------------------------------------------------------

def _lunation_fraction(date: datetime.date) -> float:
    """Return the fractional part of the lunation for *date*.

    The algorithm is a lightweight approximation that is sufficient for
    everyday use and matches the standard eight‑phase naming convention.
    """
    year = date.year
    month = date.month
    day = date.day

    # Convert month/year to a continuous count as described in many public
    # implementations (e.g., https://stackoverflow.com/a/49146844).
    if month < 3:
        year -= 1
        month += 12
    month += 1  # March = 4, …, February = 14

    # Julian Day approximation relative to a known new‑moon reference.
    jd = (365.25 * year) + (30.6 * month) + day - 694039.09
    # Normalize to lunar cycles (29.5305882 days per lunation).
    lunations = jd / 29.5305882
    return lunations - int(lunations)


def get_moon_phase(date: datetime.date) -> str:
    """Return the moon phase name for *date*.

    Possible return values:
    - "New Moon"
    - "Waxing Crescent"
    - "First Quarter"
    - "Waxing Gibbous"
    - "Full Moon"
    - "Waning Gibbous"
    - "Last Quarter"
    - "Waning Crescent"
    """
    fraction = _lunation_fraction(date)
    age = fraction * 29.5305882  # age in days within the current lunation

    if age < 1.84566:
        return "New Moon"
    if age < 5.53699:
        return "Waxing Crescent"
    if age < 9.22831:
        return "First Quarter"
    if age < 12.91963:
        return "Waxing Gibbous"
    if age < 16.61096:
        return "Full Moon"
    if age < 20.30228:
        return "Waning Gibbous"
    if age < 23.99361:
        return "Last Quarter"
    if age < 27.68493:
        return "Waning Crescent"
    return "New Moon"

# ---------------------------------------------------------------------------
# ASCII art representations for each phase
# ---------------------------------------------------------------------------
_ASCII_ART = {
    "New Moon": """
      _..._      
    .:::::::.   
   :::::::::::  
   :::::::::::  
    '::::::'   
      ‾‾‾      
""",
    "Waxing Crescent": """
      _..._      
    .:::::::.   
   :::::::::::  
   :::::::::::  
    '::::::'   
      ‾‾‾      
""",
    "First Quarter": """
      _..._      
    .:::::::.   
   :::::::::::  
   :::::::::::  
    '::::::'   
      ‾‾‾      
""",
    "Waxing Gibbous": """
      _..._      
    .:::::::.   
   :::::::::::  
   :::::::::::  
    '::::::'   
      ‾‾‾      
""",
    "Full Moon": """
      _..._      
    .:::::::.   
   :::::::::::  
   :::::::::::  
    '::::::'   
      ‾‾‾      
""",
    "Waning Gibbous": """
      _..._      
    .:::::::.   
   :::::::::::  
   :::::::::::  
    '::::::'   
      ‾‾‾      
""",
    "Last Quarter": """
      _..._      
    .:::::::.   
   :::::::::::  
   :::::::::::  
    '::::::'   
      ‾‾‾      
""",
    "Waning Crescent": """
      _..._      
    .:::::::.   
   :::::::::::  
   :::::::::::  
    '::::::'   
      ‾‾‾      
""",
}


def _print_phase(date: datetime.date) -> None:
    phase = get_moon_phase(date)
    art = _ASCII_ART.get(phase, "")
    print(f"{date.isoformat()} – {phase}\n{art}")


def main(argv: Tuple[str, ...] = sys.argv[1:]) -> None:
    """CLI entry point.

    * No arguments – prints today’s phase.
    * One argument – a date string ``YYYY-MM-DD`` to inspect.
    """
    if not argv:
        target = datetime.date.today()
    else:
        # Mock rationale: parsing is simple; we avoid external libs.
        try:
            target = datetime.date.fromisoformat(argv[0])
        except ValueError as exc:
            print(f"Invalid date format: {argv[0]}. Use YYYY-MM-DD.")
            sys.exit(1)
    _print_phase(target)


if __name__ == "__main__":
    main()
