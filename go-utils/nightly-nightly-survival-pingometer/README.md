# Nightly Survival Pingometer

**What it does**

`pingometer` concurrently checks a list of hosts (defaulting to a few well‑known services) and reports a *Survival Rating* – a playful score that tells you how prepared your network is for the end of days.

**Why it’s useful**

- Quickly verify connectivity to multiple endpoints.
- Shows results in a fun, themed way (e.g., *“Radiation‑Free”*, *“Barely Breathing”*).
- Fully concurrent, making the checks fast even for long host lists.

**Installation**

```bash
# Clone the repository (or copy the utility folder) and build
git clone https://github.com/polsala/ApocalypsAI.git
cd go-utils/nightly-survival-pingometer
go build -o pingometer ./src/main.go
```

**Usage**

```bash
# Use default host list
./pingometer

# Provide your own hosts (space‑separated)
./pingometer example.com 8.8.8.8 bad.host
```

**Output example**

```
Checking 3 hosts...
[✔] example.com reachable
[✖] bad.host unreachable
[✔] 8.8.8.8 reachable

Survival Rating: 66% – "Radiation‑Free"
```

**Testing**

Run the deterministic unit tests (they use mocked dialers, no real network calls):

```bash
go test ./tests
```

**License**

MIT – see LICENSE file in the repository root.
