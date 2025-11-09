# Nightly Repo Health Potion Brewer

## 🧙‍♂️ What is this?

The ApocalypsAI Nightly Integrator presents the **Repo Health Potion Brewer**! This whimsical-yet-useful utility scans your local repository for common 'ailments' – signs of neglect or missing essential files – and suggests powerful 'potions' to restore its vitality and ensure it's ready for any digital apocalypse.

Think of it as a magical check-up for your codebase, ensuring it has all the necessary scrolls, charms, and elixirs to thrive.

## ✨ Features

*   **Ailment Detection**: Identifies missing `README.md`, `LICENSE`, `.gitignore`, `CHANGELOG.md`, and placeholder `CONTRIBUTING.md` files.
*   **Potion Suggestions**: Provides actionable advice and commands to remedy each detected ailment.
*   **Whimsical Naming**: All ailments and potions are given charming, magical names to make repo maintenance a delightful quest.

## 🚀 Usage

1.  Navigate to your repository's root directory in your terminal.
2.  Run the `potion_brewer.py` script:

    ```bash
    python src/potion_brewer.py
    ```

    (Alternatively, you can specify a path to a repository:
    `python src/potion_brewer.py --path /path/to/your/repo`)

## 🧪 Example Output

```
Brewing health potions for your repository...

Detected Ailments and Suggested Potions:

- Ailment: Missing Readme of Lore (README.md not found)
  Potion: Scroll of Introduction (Action: Create a README.md file to introduce your project.)

- Ailment: Absence of Legal Charm (LICENSE not found)
  Potion: Tincture of Openness (Action: Add a LICENSE file to define your project's legal terms. Consider MIT or Apache-2.0.)

- Ailment: Unfiltered Artifacts (.gitignore not found)
  Potion: Elixir of Cleanliness (Action: Create a .gitignore file to prevent unwanted files from being committed.)

- Ailment: Silent Contribution Scroll (CONTRIBUTING.md exists but is a placeholder)
  Potion: Philter of Collaboration (Action: Flesh out CONTRIBUTING.md with guidelines for contributors.)

- Ailment: Forgotten Changelog (CHANGELOG.md not found)
  Potion: Chronicle of Progress (Action: Create a CHANGELOG.md to document all notable changes.)

Your repository needs some magical attention!
```

## 📜 Ailments & Potions Glossary

| Ailment                       | Description                                   | Potion                      | Suggested Action                                                               |
| :---------------------------- | :-------------------------------------------- | :-------------------------- | :----------------------------------------------------------------------------- |
| Missing Readme of Lore        | `README.md` is absent.                        | Scroll of Introduction      | Create a `README.md` to introduce your project.                                |
| Absence of Legal Charm        | `LICENSE` file is missing.                    | Tincture of Openness        | Add a `LICENSE` file (e.g., MIT, Apache-2.0).                                  |
| Unfiltered Artifacts          | `.gitignore` is not present.                  | Elixir of Cleanliness       | Create a `.gitignore` to exclude unwanted files.                               |
| Silent Contribution Scroll    | `CONTRIBUTING.md` is empty or a placeholder.  | Philter of Collaboration    | Flesh out `CONTRIBUTING.md` with contribution guidelines.                     |
| Forgotten Changelog           | `CHANGELOG.md` is missing.                    | Chronicle of Progress       | Create a `CHANGELOG.md` to document project changes.                           |

## 🛠️ Development

This utility is written in Python 3.11 and uses standard library modules only. Tests are self-contained and use `unittest.mock` for deterministic, offline execution.
