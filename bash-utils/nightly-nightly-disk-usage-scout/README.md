Nightly Disk Usage Scout
=========================

Overview
--------
A tiny Bash utility that reports the biggest directories (or files) under a given path. It uses the standard `du` command, sorts the results by size, and prints the top N entries. Options allow you to:

* Choose the depth to scan (`-d`)
* Limit the number of results (`-n`)
* Show human‑readable sizes (`-h`)

The script is deliberately simple and can be overridden for testing by setting the environment variable `DU_CMD` to any command that mimics `du` output.

Installation
------------
Copy the `src/main.sh` file to a location in your `$PATH` and make it executable:

    chmod +x src/main.sh
    sudo mv src/main.sh /usr/local/bin/disk-usage-scout

Usage
-----
    disk-usage-scout [options] [path]

Options:
    -d <depth>   Maximum directory depth to explore (default: 1)
    -n <count>   Number of top entries to display (default: 10)
    -h           Show sizes in human‑readable format (e.g., 1K, 2M)

If no path is supplied, the current directory is used.

Examples
--------
Show the ten largest directories up to depth 2 in the current folder:

    disk-usage-scout -d 2

Show the five biggest items in /var with human‑readable sizes:

    disk-usage-scout -n 5 -h /var

Testing
-------
Run the bundled test suite with:

    cd tests && ./test_main.sh

The test replaces the `du` command with a mock, ensuring deterministic results.
