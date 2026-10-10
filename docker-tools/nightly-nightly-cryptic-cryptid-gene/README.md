# Cryptic Cryptid Generator

A whimsical Dockerized utility that prints a randomly generated cryptid description each time it runs. Perfect for adding a touch of mystery to your terminal.

## Usage

```sh
docker build -t cryptid-generator .
docker run --rm cryptid-generator
```

Example output:

```
The Neon-Scaled Skywhale, a mysterious creature that dwells in the moonlit marshes and sings lullabies to wandering travelers.
```

## How it works

The container runs a tiny Python script that assembles a cryptid name and description from predefined parts.

## License

MIT
