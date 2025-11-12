# Git Branch Namer

Utility to generate clean, conventional Git branch names from issue titles or feature descriptions. It normalizes to kebab‑case, strips emojis, punctuation, and prefixes with a conventional type (`feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `test`, `build`). If the title starts with a known type keyword (case‑insensitive) it uses that; otherwise defaults to `feat`.

## Usage

```bash
python -m branch_namer "Add user login page"
# => feat/add-user-login-page
```

You can also import the function in your own scripts:

```python
from branch_namer import generate_branch_name
name = generate_branch_name("Fix typo in README")
print(name)  # fix/typo-in-readme
```
