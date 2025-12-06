# Nightly Planetary Age Calculator

Utility to compute your age on various planets given Earth years.

## Usage

```bash
python -m planetary_age <earth_years> <planet>
```

Example:

```bash
python -m planetary_age 30 mars
# => 15.96 years on mars
```

Supported planets (case‑insensitive):

- mercury
- venus
- earth
- mars
- jupiter
- saturn
- uranus
- neptune
- pluto

## Implementation Details

The calculator uses each planet's orbital period relative to Earth (in Earth years) and divides the supplied Earth‑year age by that factor, rounding the result to two decimal places.
