FROM rust:1.72-slim AS builder
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src ./src
RUN cargo build --release

FROM debian:bookworm-slim
COPY --from=builder /app/target/release/cryptid-finder /usr/local/bin/cryptid-finder
ENTRYPOINT ["cryptid-finder"]
