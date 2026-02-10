# Nightly Safehouse Namer

Utility that generates a whimsical post‑apocalyptic safe‑house name, e.g., "Dusty Oasis". Useful for naming servers, projects, or in‑game locations.

## Installation

```sh
go build -o safehouse-namer ./src
```

## Usage

```sh
./safehouse-namer
# Example output: "Radiant Wasteland"
```

## How it works

Combines a random adjective and noun from curated lists.

## Testing

```sh
go test ./...
```
