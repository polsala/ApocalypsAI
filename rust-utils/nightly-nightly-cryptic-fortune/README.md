# nightly-cryptic-fortune

Generate a deterministic whimsical fortune based on input text.

## Usage

cargo run -- "your input text"

or build and run:

cargo build --release
./target/release/nightly-cryptic-fortune "your input text"

The tool will output a fortune chosen deterministically from a small list.

## Example

$ nightly-cryptic-fortune "hello world"
Fortune: The stars align in your favor today.
