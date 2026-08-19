# Nightly Doom List Prioritizer

The apocalypse is chaotic, but your to-do list doesn't have to be! The `nightly-doom-list-prioritizer` is a whimsical utility that helps you sort your survival tasks by their perceived "Doom Factor." It scans your tasks for critical keywords, assigns an urgency score, and even adds a slightly sarcastic, yet motivating, comment. Because even when the world is ending, a little structure (and humor) goes a long way.

## Usage

Pipe your list of tasks to the script, or provide a file as an argument.

```bash
# From stdin
echo "Repair the temporal rift stabilizer" | ./src/doom_list_prioritizer.sh
echo -e "Scavenge for water filters\nFortify the shelter perimeter\nOrganize the canned goods" | ./src/doom_list_prioritizer.sh

# From a file
./src/doom_list_prioritizer.sh my_apocalypse_tasks.txt
```

### Example `my_apocalypse_tasks.txt`:
```
Repair the temporal rift stabilizer
Scavenge for water filters
Fortify the shelter perimeter
Organize the canned goods
Recharge the solar lanterns
Investigate the strange hum from sector 7
Clean the mutant-proof windows
```

## Output

The script will output a prioritized list, showing the Doom Factor, a whimsical comment, and the original task.

```
--- Doom List Prioritization Report ---
Doom Factor: 5 | Urgency: CRITICAL | Comment: The fabric of reality is fraying. This cannot wait. | Task: Repair the temporal rift stabilizer
Doom Factor: 4 | Urgency: CRITICAL | Comment: A whisper from the void suggests this is paramount. | Task: Investigate the strange hum from sector 7
Doom Factor: 3 | Urgency: HIGH     | Comment: The void hungers for your procrastination. | Task: Fortify the shelter perimeter
Doom Factor: 2 | Urgency: HIGH     | Comment: Don't let the temporal distortions distract you. | Task: Scavenge for water filters
Doom Factor: 1 | Urgency: LOW      | Comment: Even in the apocalypse, some things can wait... probably. | Task: Recharge the solar lanterns
Doom Factor: 1 | Urgency: LOW      | Comment: The cosmic dust bunnies can wait. Or can they? | Task: Organize the canned goods
Doom Factor: 1 | Urgency: LOW      | Comment: The cosmic dust bunnies can wait. Or can they? | Task: Clean the mutant-proof windows
```

## Configuration

The script uses internal keyword lists and comments. You can modify `src/doom_list_prioritizer.sh` to customize these.

## Development

To run tests, navigate to the utility's directory and execute the test script:

```bash
./tests/test_doom_list_prioritizer.sh
```
