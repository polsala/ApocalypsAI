# nightly-dockerfile-linter

A lightweight Go CLI that lints Dockerfiles for common best‑practice violations.

Usage

go run src/main.go path/to/Dockerfile

or

cat Dockerfile | go run src/main.go

The tool prints a list of issues or OK if none are found.

Lint Rules

- Dockerfile must contain a FROM instruction.
- Dockerfile must contain a CMD or ENTRYPOINT instruction.
- RUN apt-get update should be followed by apt-get install -y in the same line or next line.
- No ADD instructions; use COPY instead.

License

MIT
