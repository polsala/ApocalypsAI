# Nightly Rocket Launcher

A whimsical Rust CLI that simulates a projectile launch.  Given an initial speed (m/s) and launch angle (degrees), it prints the time of flight, maximum height, and horizontal range.

## Usage

```bash
cargo run --quiet -- <speed_m_s> <angle_deg>
```

## Example

```bash
cargo run --quiet -- 100 45
```

Output

```
Time of flight: 14.42 s
Max height: 255.10 m
Range: 1019.40 m
```

The program uses the standard physics equations for projectile motion in a vacuum (no air resistance).
