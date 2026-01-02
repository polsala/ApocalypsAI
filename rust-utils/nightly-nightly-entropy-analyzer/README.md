# nightly‑entropy‑analyzer

**What it does**

`nightly‑entropy‑analyzer` reads data from a file (or standard input) and calculates the Shannon entropy in bits per byte.  It prints the numeric value and, if the entropy is **≥ 4.5 bits/byte**, it warns that the input looks like high‑entropy (e.g., a password, key, or compressed data).

**Why it’s useful**

- Quickly gauge the randomness of a string or file.
- Spot accidentally leaked secrets in logs.
- Fun for the curious who wonder how “random” their data really is.

**Installation**

```bash
# From the repository root
cd rust-utils/nightly-entropy-analyzer
cargo build --release
# The binary will be at target/release/nightly-entropy-analyzer
```

**Usage**

```bash
# From a file
./nightly-entropy-analyzer path/to/file.txt

# From stdin (e.g., pipe)
echo "hello world" | ./nightly-entropy-analyzer -
```

The `-` argument tells the tool to read from standard input.

**Output example**

```
Entropy: 3.1808 bits/byte
```

If the entropy is high:

```
Entropy: 4.78 bits/byte
⚠️ High‑entropy data detected! This may be a secret or compressed content.
```

**Testing**

Run the built‑in test suite with:

```bash
cargo test
```

---

*Created by the ApocalypsAI Nightly Integrator.*
