Nightly Radiation Exposure Tracker
A tiny CLI tool that reads a CSV of radiation exposure events and reports the total dose. Optionally warns if a threshold is exceeded.

Usage:
  nightly-radiation-exposure-tracker <file> [threshold]

The CSV should have two columns: timestamp,dose (dose in mSv). Example:
2023-01-01T12:00:00Z,0.5
2023-01-02T08:30:00Z,1.2

If a threshold is provided, the tool prints a warning when total dose > threshold.
