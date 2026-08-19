Nightly Disk Dread Alarmer
==========================

Overview
--------
`nightly-disk-dread-alarmer` is a tiny Bash script that inspects the size of a given directory and emits a whimsical warning if the directory grows beyond a user‑defined threshold.  It is useful for keeping an eye on log folders, cache directories, or any place where data can silently accumulate and threaten the stability of your system.

Installation
------------
Copy the `src/main.sh` script to a location in your `$PATH` and make it executable:

    mkdir -p ~/bin
    cp src/main.sh ~/bin/disk-dread-alarmer
    chmod +x ~/bin/disk-dread-alarmer

Usage
-----
    disk-dread-alarmer <directory> [threshold_kb]

* `<directory>` – Path to the directory you want to monitor.
* `[threshold_kb]` – Optional size limit in kilobytes (default: 102400 KB, i.e., 100 MiB).

If the directory exceeds the threshold the script prints a warning prefixed with a skull emoji; otherwise it prints a reassuring check‑mark.

Example
-------
    $ disk-dread-alarmer /var/log 50000
    ✅  /var/log is within safe limits.

    $ disk-dread-alarmer /var/log 1000
    ⚠️  The abyss of /var/log grows to 12345K!

Testing
-------
Run the bundled test suite with:

    cd tests
    ./test_main.sh

The tests are deterministic and do not touch the real filesystem.
