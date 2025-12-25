# nightly-disk-warden-alert

Utility that checks disk usage for specified directories and prints a skull‑and‑crossbones warning when usage exceeds a given percentage. Perfect for keeping your post‑apocalyptic server alive.

## Usage

```sh
./src/main.sh config.txt
```

`config.txt` format (one entry per line):

```
/path/to/dir 80
/home 90
```

The script will report any filesystem that is at or above the threshold.

## Example

```
$ cat config.txt
/var 75
/home 85

$ ./src/main.sh config.txt
⚠️  /var is at 78% – beware the wasteland!
💀  /home is at 90% – the void beckons!
```

## Testing

Run the test suite:

```sh
bash tests/test_main.sh
```
