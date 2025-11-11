# Nightly Docstring Sentinel

## Purpose
The Nightly Docstring Sentinel is a vigilant utility designed to improve code documentation across your Python projects. It scans specified directories for Python files, identifying functions and classes that are either missing docstrings entirely or possess docstrings deemed too short or generic to be truly useful. By highlighting these 'deficiencies', the Sentinel helps maintainers ensure that the codebase remains clear, understandable, and maintainable for current and future contributors.

## How to Use
To unleash the Sentinel, navigate to its directory and run the `sentinel.py` script, providing the path to the directory you wish to scan.

```bash
python src/sentinel.py /path/to/your/repository
```

### Configuration
The `src/sentinel.py` script includes basic configuration parameters that can be adjusted:
- `MIN_DOCSTRING_LENGTH`: The minimum character length a docstring must have to be considered 'sufficient'. Docstrings shorter than this will be flagged.
- `IGNORED_PATHS`: A list of directory names (e.g., `venv`, `.git`, `tests`) to exclude from the scan. This prevents the Sentinel from getting distracted by non-source code or test files.

## Output
The Sentinel reports its findings in a clear, human-readable format, listing each file with identified docstring deficiencies. For each deficiency, it specifies the type (class or function), its name, and the line number where it was found.

### Example Output:
```
Scanning directory: /path/to/your/repository

--- Docstring Deficiencies Found ---

File: my_project/module_a.py
  - Function 'calculate_sum' (line 10): Missing docstring.
  - Class 'MyClass' (line 25): Docstring too short or generic.

File: my_project/sub_dir/utility.py
  - Function 'helper_func' (line 5): Missing docstring.

No deficiencies found in other files.
```

Let the Sentinel guide your codebase to a brighter, better-documented future!
