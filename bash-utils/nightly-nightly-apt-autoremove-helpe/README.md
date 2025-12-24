Nightly Apt Autoremove Helper
================================

Overview
--------
This tiny Bash utility inspects the system's package manager (APT) and reports which packages would be removed by an `apt-get autoremove` operation. It runs in *dry‑run* mode by default, merely listing the packages. With the `--apply` flag it will actually execute `apt-get autoremove -y` to clean the system.

Why use it?
------------
* Quickly see what would be removed without invoking the real command.
* Integrate into CI/CD or cron jobs to keep build agents tidy.
* Safe default – nothing is changed unless you explicitly ask.

Installation
------------
Copy the `src/main.sh` script to a location in your `$PATH` and make it executable:

    chmod +x src/main.sh
    sudo mv src/main.sh /usr/local/bin/apt-autoremove-helper

Usage
-----
    apt-autoremove-helper [--dry-run] [--apply]

Options
-------
* `--dry-run` (default) – Show the packages that would be removed.
* `--apply` – Actually run `apt-get autoremove -y` after the dry‑run summary.

Examples
--------
Dry‑run (default):

    $ apt-autoremove-helper
    Packages that would be removed:
      libfoo1
      libbar2

Apply the changes:

    $ sudo apt-autoremove-helper --apply
    Packages that would be removed:
      libfoo1
      libbar2
    Proceeding with apt-get autoremove -y ...

Testing
-------
Run the bundled test suite with:

    bash tests/test_main.sh

The tests mock the `apt-get` binary, so they are safe to run on any machine.
