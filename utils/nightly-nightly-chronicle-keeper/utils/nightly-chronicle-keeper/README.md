# Nightly Chronicle Keeper

## For the Lone Wanderer, the Scavenger, the Survivor.

In these trying times, keeping track of your journey, discoveries, and the occasional mutant encounter is paramount. The Nightly Chronicle Keeper is a simple, command-line utility designed to help you log your daily events, thoughts, and observations in the wasteland. Each entry is automatically timestamped, ensuring your chronicles are always in order.

### Features:
- **Timestamped Entries**: Every log entry is automatically marked with the date and time of its creation.
- **Simple Interface**: Easy to use from your terminal, no complex setup required.
- **Persistent Log**: All your chronicles are saved to a plain text file, ready for review.

### Installation & Usage:

1.  **Navigate to the utility directory**: 
    ```bash
    cd utils/nightly-chronicle-keeper/src
    ```

2.  **Add a new chronicle entry**: 
    ```bash
    python chronicle.py add "Found a pristine can of pre-war beans near the old gas station. A good day."
    ```
    or
    ```bash
    python chronicle.py add "The rad-storm passed. Managed to salvage some copper wire from the ruins."
    ```

3.  **View all your chronicles**: 
    ```bash
    python chronicle.py view
    ```

### Log File Location:
By default, your chronicles will be stored in `chronicle.log` within the `src/` directory.

### For the Future:
May your chronicles be long and your survival assured.
