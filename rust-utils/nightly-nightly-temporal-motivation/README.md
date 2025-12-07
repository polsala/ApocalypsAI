Temporal Motivation Mixer
========================

A Rust CLI tool that generates time-based affirmations with optional chaos mode.

Usage:
  temporal-motivation-mixer [OPTIONS]

Options:
  -c, --chaos       Add random temporal distortions to messages
  -h, --help        Print help
  -V, --version     Print version

Examples:
  $ temporal-motivation-mixer
  It's 3:45 PM - Time to conquer the afternoon!

  $ temporal-motivation-mixer -c
  It's 3:45 PM ± 2h (Temporal Anomaly Detected) - Time to bend reality!
