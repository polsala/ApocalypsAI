# Nightly Digital Dust Bunny Sweeper

## Summary

The `nightly-digital-dust-bunny-sweeper` is a whimsical-yet-useful utility designed to help you keep your system tidy. It scans common temporary directories and old log file locations for files that haven't been accessed in a while (our 'digital dust bunnies') and reports on their presence, size, and age. It *does not delete* anything, only reports, giving you the power to decide what to sweep away.

## Usage

To run the sweeper with default settings (scans common temp/log dirs for files older than 30 days):

```bash
bash src/dust_bunny_sweeper.sh
```

### Customizing Directories

You can specify custom directories to scan by passing them as arguments:

```bash
bash src/dust_bunny_sweeper.sh /path/to/my/temp /var/log/old_app
```

### Customizing Age Threshold

Set the `DUST_BUNNY_AGE_DAYS` environment variable to change the age threshold (in days) for what constitutes a 'dust bunny'. Default is 30 days.

```bash
DUST_BUNNY_AGE_DAYS=7 bash src/dust_bunny_sweeper.sh
```

### Example Output

```
🧹 Scanning for lurking digital dust bunnies...

🔍 Found a colony of 3 digital dust bunnies, weighing in at 1.5M!

Top 3 chonky dust bunnies:
- 1.0M  /tmp/old_cache/large_temp_file.dat (last accessed 45 days ago)
- 512K  /var/log/stale_app.log (last accessed 32 days ago)
- 12K   /home/user/.cache/old_data.tmp (last accessed 60 days ago)

✨ Your system is looking cleaner, even if it's just a report! ✨
```

## Development & Testing

To run the automated tests:

```bash
bash tests/test_sweeper.sh
```

The tests create a temporary environment to simulate stale files and verify the script's reporting capabilities without affecting your actual system.
