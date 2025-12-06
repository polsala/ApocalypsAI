# Dependency Doom-Scroller

## The Prophecy of Package Rot

In the ever-shifting sands of the digital realm, dependencies lurk like ancient, forgotten gods. The `Dependency Doom-Scroller` is your nightly oracle, peering into the very soul of your project's `requirements.txt` to foresee the impending 'Great Dependency Collapse'. It warns you when your packages are lagging behind, trapped in a bygone era, lest your project succumb to the ravages of time and incompatibility.

## What it Does

This utility scans your project directory for a `requirements.txt` file. For each declared package, it consults the cosmic archives (PyPI) to determine if a newer, more potent version exists. If your current version is deemed 'ancient' or 'outdated', the Doom-Scroller will issue a dramatic, yet actionable, warning, guiding you towards the path of upgrade and stability.

## Why it's Useful

*   **Prevents 'Dependency Rot'**: Proactively identifies outdated packages before they cause critical vulnerabilities or compatibility issues.
*   **Maintains Project Health**: Encourages regular updates, keeping your project robust and secure.
*   **Whimsical Warnings**: Delivers crucial information with a touch of apocalyptic flair, making maintenance less mundane.
*   **Self-Contained**: A standalone Python script, easy to integrate into any workflow.

## Usage

1.  Navigate to your project's root directory (or specify one).
2.  Run the `doom_scroller.py` script:

    ```bash
    python src/doom_scroller.py
    # Or, to scan a specific directory:
    # python src/doom_scroller.py --directory /path/to/your/project
    ```

## Example Output

```
Scanning for signs of dependency decay...

--- The Scrolls of Prophecy Reveal ---

🚨 WARNING: The ancient scroll for 'requests' (v2.25.1) is crumbling! A newer, more powerful version (v2.28.1) has emerged from the cosmic dust. Upgrade to avoid the 'Dependency Collapse'!

✅ All clear for 'pyyaml'. Its cosmic alignment is stable (v5.4.1).

⚠️ CAUTION: 'black' (v21.10b0) is showing signs of temporal distortion! The future holds v22.3.0. Consider an upgrade before the 'Formatting Anomaly' strikes!

⚠️ CAUTION: 'unpinned-package' has no version specified. The future is uncertain! (Consider pinning a version)

--- End of Prophecy ---

May your dependencies ever be current, and your project endure the ages.
```
