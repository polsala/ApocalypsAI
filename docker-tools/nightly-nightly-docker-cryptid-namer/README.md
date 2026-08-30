# Cryptid Namer

A whimsical Dockerized utility that prints a random post‑apocalyptic cryptid name each time it runs. Perfect for naming secret bases, code‑names, or just for fun.

## Usage

```sh
docker build -t cryptid-namer .
docker run --rm cryptid-namer
```

Each execution outputs a name like `Radiant Wasteland Wyrm` or `Gloomy Dust Devil`.

## How it works

The container runs a tiny Python script that selects a random adjective and creature from predefined lists.
