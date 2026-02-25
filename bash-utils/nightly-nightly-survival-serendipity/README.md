# Nightly Survival Serendipity Spinner

A whimsical Bash utility that helps you decide your next apocalyptic task based on your current "mood" or "energy level". Feeling low? Get a suggestion for recuperation. Full of high-octane survival spirit? Get a task for fortifying or scavenging!

## Usage

Run the script with your current mood as an argument:

```bash
./src/serendipity_spinner.sh <mood>
```

Replace `<mood>` with one of the following: `low`, `medium`, or `high`. The mood input is case-insensitive.

## Examples

```bash
# Feeling a bit drained?
./src/serendipity_spinner.sh low
# Output: Your Serendipity Spinner suggests: Clean and maintain weapons

# Ready for some moderate activity?
./src/serendipity_spinner.sh medium
# Output: Your Serendipity Spinner suggests: Clean and maintain weapons

# Full of energy and ready to tackle big challenges?
./src/serendipity_spinner.sh high
# Output: Your Serendipity Spinner suggests: Fortify shelter defenses
```

*(Note: Actual suggestions will vary due to the randomized nature when not in a test environment, but will always align with the chosen mood's task categories. The examples above reflect deterministic output when `shuf` is mocked.)*

## Moods and Associated Tasks

The spinner categorizes tasks by energy level:

*   **Low Energy Tasks**: Focus on recuperation, organization, learning, and light maintenance.
    *   Examples: "Rest and recuperate", "Organize inventory", "Tend to garden/crops", "Clean and maintain weapons", "Study survival guides".
*   **Medium Energy Tasks**: Involve moderate physical or mental effort, essential repairs, and local scouting.
    *   Examples: "Scavenge for supplies", "Repair essential equipment", "Organize inventory", "Scout immediate perimeter", "Craft useful tools", "Tend to garden/crops", "Clean and maintain weapons".
*   **High Energy Tasks**: Require significant effort, risk, or strategic planning.
    *   Examples: "Scavenge for supplies", "Fortify shelter defenses".

## Installation

1.  Navigate to the `bash-utils/nightly-survival-serendipity-spinner/` directory.
2.  Make the script executable:
    ```bash
    chmod +x src/serendipity_spinner.sh
    ```
3.  Run it as shown in the Usage section.

## Development & Testing

To run the automated tests:

```bash
./tests/test_serendipity_spinner.sh
```

The tests are deterministic thanks to a mocked `shuf` command, ensuring consistent results regardless of actual randomness.
