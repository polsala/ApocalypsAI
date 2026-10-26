# Apocalypse Day Counter

A tiny Dockerized utility that tells you how many days have passed since the Great Collapse. Provide a date (YYYY‑MM‑DD) as an argument; if omitted, it uses today. Perfect for post‑apocalyptic journaling or role‑play.

## Usage

```sh
docker build -t apocalypse-day-counter .
docker run --rm apocalypse-day-counter 2020-01-01
```

Output:

```
Days since the Great Collapse: 2500
```

## Build & Test

```sh
./tests/test.sh
```
