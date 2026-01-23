FROM rust:1.70

WORKDIR /usr/src/app

COPY Cargo.toml ./
COPY src/ ./src/

RUN cargo build --release

CMD ["./target/release/rustdbx"]
