# Nightly Dependency Decontaminator

## Summary

In the lean, resource-scarce world of post-apocalyptic development, every byte counts. The `nightly-dep-decontaminator` is a Dockerized utility designed to scan your project's dependencies (specifically Python `requirements.txt` for now) and flag packages that are deemed "too heavy" or "unnecessary" for a truly minimal survival stack. It suggests leaner alternatives where possible, helping you keep your digital footprint light and efficient.

## Usage

1.  **Prepare your project**: Ensure your Python project has a `requirements.txt` file in its root.
2.  **Build the Docker image**:
    ```bash
    docker build -t nightly-dep-decontaminator .
    ```
3.  **Run the decontaminator**:
    Mount your project directory to `/app/project` inside the container.
    ```bash
    docker run --rm -v "$(pwd)/your_project_path:/app/project" nightly-dep-decontaminator
    ```
    Replace `your_project_path` with the actual path to your project's root directory.

    The utility will output a report to `stdout` detailing any identified heavy dependencies and suggested alternatives.

## Configuration

The utility uses an internal `config.json` file to define "heavy" packages and their "lean" alternatives. You can customize this file by modifying `src/config.json` before building the Docker image.

Example `src/config.json`:
```json
{
  "heavy_packages": {
    "django": "Consider Flask or FastAPI for lighter web frameworks.",
    "numpy": "If only basic array ops are needed, explore `array` module or custom implementations.",
    "pandas": "For simple CSV/data handling, `csv` module or custom parsing might suffice.",
    "requests": "For basic HTTP, `urllib.request` is built-in and lighter.",
    "scipy": "Heavy scientific library; only include if absolutely critical."
  },
  "unnecessary_packages": [
    "debugpy",
    "pytest",
    "black",
    "flake8"
  ]
}
```

## How it works

The Docker container runs a Python script (`src/decontaminator.py`) that:
1.  Looks for `requirements.txt` in the mounted `/app/project` directory.
2.  Parses the `requirements.txt` to extract package names.
3.  Compares these package names against the `heavy_packages` and `unnecessary_packages` defined in `src/config.json`.
4.  Generates a report with warnings and suggestions.

## Development & Testing

To run tests, execute `tests/test_decontaminator.sh`. This script builds the Docker image and runs it against mock `requirements.txt` files to verify its functionality.
```bash
./tests/test_decontaminator.sh
```
