# Nightly Mutagenic Flora Identifier (nmfi)

`nmfi` is a high-performance command-line utility designed for the discerning wasteland botanist. It helps identify unknown flora by matching observed characteristics against a curated database of known (and often peculiar) plant life. Avoid a nasty surprise or discover a hidden boon!

## Features

*   **Characteristic-based Identification**: Input observed traits like color, shape, glow, and sound.
*   **Whimsical Flora Database**: Contains entries for common (and uncommon) post-apocalyptic plant species.
*   **Property Revelation**: Learn if a plant is edible, poisonous, hallucinogenic, or possesses other strange mutagenic properties.
*   **Fast & Efficient**: Built with Rust for blazing-fast identification.

## Installation

To install `nmfi`, you'll need Rust and Cargo installed. If you don't have them, visit [rustup.rs](https://rustup.rs/).

```bash
cargo install nightly-mutagenic-flora-id
```

Alternatively, clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-mutagenic-flora-id
cargo build --release
./target/release/nmfi --help
```

## Usage

Run `nmfi` with various characteristic flags to identify flora.

```bash
nmfi --help
```

**Examples:**

1.  **Identify a glowing, dark-purple, bell-shaped plant with a faint hum:**

    ```bash
nmfi --color dark-purple --shape bell --glow true --sound "faint-hum"
    ```

    *Expected Output (or similar):*

    ```
    Identified Flora:
    - Name: Gloom Bloom
      Properties: Poisonous, Causes temporary blindness
    ```

2.  **Look for edible plants that glow:**

    ```bash
nmfi --glow true
    ```

    *Expected Output (or similar):*

    ```
    Identified Flora:
    - Name: Gloom Bloom
      Properties: Poisonous, Causes temporary blindness
    - Name: Shimmer Shroom
      Properties: Edible, Grants enhanced night vision for 1 hour
    - Name: Void Blossom
      Properties: Temporal Displacement, Highly Unstable
    - Name: Glimmer Grass
      Properties: Edible, Provides minor healing
    - Name: Crimson Spore
      Properties: Highly Toxic, Causes rapid cellular decay
    ```
    *(Note: The tool will list all matches; you'll need to filter by desired properties manually if not specified in the query.)*

3.  **Query for a plant with a specific sound:**

    ```bash
nmfi --sound "soft-rustle"
    ```

4.  **No matching characteristics:**

    ```bash
nmfi --color blue --shape square
    ```

    *Expected Output:*

    ```
    No flora identified with the given characteristics.
    ```

## Contributing

Feel free to expand the `FLORA_DB` with new, imaginative, and dangerous flora entries! Pull requests are welcome.
