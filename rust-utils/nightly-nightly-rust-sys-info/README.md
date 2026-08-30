# nightly-rust-sys-info

A whimsical yet useful standalone utility built with Rust. This command-line interface (CLI) tool provides a quick and efficient way to gather and display essential system information.

## Features

*   **System Name**: Displays the operating system name.
*   **Kernel Version**: Shows the kernel version.
*   **CPU Information**: Lists CPU model and core count.
*   **Memory Usage**: Reports total, available, and used RAM.
*   **Disk Usage**: Displays total and used space for the root filesystem.

## Installation

1.  **Prerequisites**: Ensure you have Rust and Cargo installed.
    ```bash
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
    ```

2.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```

3.  **Build the utility**:
    ```bash
    cargo build --release
    ```

4.  **Run the utility**:
    The executable will be located in `target/release/nightly-rust-sys-info`.
    ```bash
    ./target/release/nightly-rust-sys-info
    ```

## Usage

Run the command without any arguments to display all system information.

```bash
nightly-rust-sys-info
```

## Contributing

Contributions are welcome! Please follow the standard ApocalypsAI contribution guidelines.

## License

This project is licensed under the MIT License.
