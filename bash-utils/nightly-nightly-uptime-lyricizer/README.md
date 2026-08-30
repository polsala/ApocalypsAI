# nightly-uptime-lyricizer

Utility that reads system uptime and prints a whimsical message describing how long the system has been alive.

## Usage

```sh
./src/uptime_lyricizer.sh
```

Optional environment variable `UPTIME_FILE` can point to a file containing uptime seconds (like `/proc/uptime`) for testing.

## Example

```
$ ./src/uptime_lyricizer.sh
The system has been alive for 3 days, 4 hours, 12 minutes. Time flies!
```
