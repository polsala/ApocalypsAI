# Nightly Bunker Buddy Backup Checker

## Overview

In these uncertain times, your digital survival supplies are paramount! The `nightly-bunker-buddy-backup-checker` is your trusty companion, ensuring that your most critical files and directories are safely tucked away in your designated 'bunker' (backup location). It provides a quick status report, letting you know if your backups are up-to-date, missing, or in need of a refresh.

Think of it as your digital inventory manager for the apocalypse – making sure your blueprints, manifestos, and cat videos are ready for the long haul.

## Usage

```bash
python src/checker.py --source /path/to/critical/data --backup /path/to/your/bunker
```

### Arguments:

*   `--source <path>`: The path to the critical file or directory you want to check. Can be specified multiple times.
*   `--backup <path>`: The path to your backup 'bunker' directory.

## Examples

Check a single file:

```bash
python src/checker.py --source ~/my_secret_plans.txt --backup /mnt/external_drive/bunker_backups
```

Check multiple files and a directory:

```bash
python src/checker.py \
    --source ~/my_secret_plans.txt \
    --source ~/bunker_manifesto.md \
    --source ~/important_configs/ \
    --backup /mnt/external_drive/bunker_backups
```

## How it Works

1.  It verifies the existence of your 'bunker' directory.
2.  For each specified source (file or directory), it checks if a corresponding item exists within the 'bunker'.
3.  If both exist, it compares their last modification times. If the source is newer than its backup, it's considered 'outdated'.
4.  It reports the status for each item: `UP-TO-DATE`, `OUTDATED`, `MISSING IN BUNKER`, or `SOURCE MISSING`.

Stay vigilant, survivor!
