# Nightly Apocalypse Cipher

**Overview**
A tiny Rust CLI that transforms any input string into a stylized post‑apocalyptic cipher. Each alphabetic character is replaced by a fixed symbolic counterpart, giving your messages a gritty, survival‑ist vibe.

**Installation**
```bash
# Clone the repository (or copy the utility folder into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-apocalypse-cipher

# Build the binary
cargo build --release
```
The compiled binary will be located at `target/release/nightly-apocalypse-cipher`.

**Usage**
```bash
./target/release/nightly-apocalypse-cipher "Your message here"
```
Example:
```bash
$ ./target/release/nightly-apocalypse-cipher "Hello World"

h3||0 w0rld
```

**Mapping Table**
| Letter | Symbol |
|--------|--------|
| a | @ |
| b | # |
| c | $ |
| d | % |
| e | 3 |
| f | & |
| g | 9 |
| h | h |
| i | ! |
| j | * |
| k | ( |
| l | \| |
| m | m |
| n | n |
| o | 0 |
| p | p |
| q | q |
| r | r |
| s | 5 |
| t | 7 |
| u | u |
| v | v |
| w | w |
| x | x |
| y | y |
| z | 2 |

Non‑alphabetic characters are left unchanged.

**Testing**
Run the test suite with:
```bash
cargo test
```
All tests are deterministic and run offline.
