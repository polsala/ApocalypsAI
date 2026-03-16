# Nightly Shelter Capacity Planner

A whimsical CLI tool to determine if your post‑apocalyptic shelter can sustain a group of survivors given water and food supplies.

## Installation

```sh
cargo build --release
```

## Usage

```sh
nightly-shelter-capacity-planner <people> <water_per_day_liters> <total_water_liters> <food_per_day_kcal> <total_food_kcal> <days>
```

Example:

```sh
nightly-shelter-capacity-planner 5 2.5 500 2000 100000 30
```

The program prints `Survivable: Yes` if the supplies are sufficient, otherwise `Survivable: No`.

## How it works

The tool multiplies the number of people by daily consumption and the number of days, then checks if the total supplies meet or exceed those requirements.

## Testing

```sh
cargo test
```
