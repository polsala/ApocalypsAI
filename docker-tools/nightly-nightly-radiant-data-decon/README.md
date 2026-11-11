# Nightly Radiant Data Decontaminator

## Summary

The `nightly-radiant-data-decon` is a containerized utility designed to cleanse and normalize text-based data files. In the post-apocalyptic digital wasteland, data can become corrupted, filled with 'digital radiation' – malformed characters, excessive whitespace, and temporal echoes from decaying systems. This tool helps survivors make sense of their precious data by decontaminating it.

## Features

-   **Character Sanitization**: Removes non-printable ASCII characters and attempts to handle common encoding issues.
-   **Whitespace Normalization**: Collapses multiple spaces/tabs into single spaces, trims line-ending whitespace, and removes entirely empty lines.
-   **Temporal Echo Removal**: Filters out common repetitive patterns or garbled timestamps that often plague salvaged data logs.
-   **Containerized**: Easy to deploy and run consistently across different environments using Docker.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-radiant-data-decon` directory and build the Docker image:

```bash
docker build -t radiant-data-decon .
```

### 2. Prepare Data Volumes

You'll need an input directory containing the files you wish to decontaminate and an empty output directory where the cleaned files will be placed.

For example:

```bash
mkdir input_data
mkdir output_data
echo -e "Hello  World!\n\nThis is a test.\x00\x01\x02\n  More data  with   extra spaces.  \n[ECHO] 2023-10-27 10:00:00 [ECHO]" > input_data/contaminated.txt
```

### 3. Run the Decontaminator

Run the Docker container, mounting your input and output directories:

```bash
docker run --rm \
  -v "$(pwd)/input_data:/app/input" \
  -v "$(pwd)/output_data:/app/output" \
  radiant-data-decon
```

-   `--rm`: Automatically remove the container when it exits.
-   `-v "$(pwd)/input_data:/app/input"`: Mounts your local `input_data` directory to `/app/input` inside the container.
-   `-v "$(pwd)/output_data:/app/output"`: Mounts your local `output_data` directory to `/app/output` inside the container.

After execution, your `output_data` directory will contain the decontaminated versions of the files from `input_data`.

## Configuration (Advanced)

The `decontaminator.py` script can be modified to adjust cleaning rules, such as adding more complex regex patterns for 'temporal echoes' or different character replacement strategies. Rebuild the Docker image after any changes to `src/decontaminator.py`.

## Development & Testing

See `tests/test_decontaminator.sh` for an example of how to run automated tests for this utility.
