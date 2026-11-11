# Nightly Radiation Report

**Utility:** `radiation_report.sh`

Generate a post‑apocalyptic style radiation report for any file. The report includes:

* File size in bytes
* Number of lines
* A deterministic "radiation level" (0‑100 µSv/h) derived from the file's SHA‑256 hash

## Usage

```bash
./radiation_report.sh <path-to-file>
```

### Example

```bash
$ cat example.txt
Apocalypse is near.
Stay safe.
$ ./radiation_report.sh example.txt
Radiation Report for example.txt
Size: 31 bytes
Lines: 2
Radiation Level: 42 µSv/h
```

The radiation level will always be the same for the same file content, making the tool suitable for automated checks or just a bit of fun.

## Requirements

* Bash (≥ 4.0)
* `sha256sum` (standard on GNU coreutils)
* `stat` (or fallback to `wc -c`)

## License

MIT © ApocalypsAI
