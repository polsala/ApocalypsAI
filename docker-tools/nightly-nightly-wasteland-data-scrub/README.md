# Nightly Wasteland Data Scrubber

## Summary

The `nightly-wasteland-data-scrubber` is a containerized utility designed to process raw, often noisy, data logs and sensor readings collected from the post-apocalyptic wasteland. It extracts critical information such as resource types, quantities, and locations, presenting them in a clean, standardized CSV format.

This tool is essential for making sense of fragmented data, helping survivors prioritize scavenging efforts and manage resources more effectively.

## How it Works

The scrubber uses Python with regular expressions to identify and extract specific patterns from text-based input files. It looks for lines containing `DATA:` and then parses `[RESOURCE:X]`, `Amount: Y units`, and `Location: (COORD:A,B)` patterns. The extracted data is then formatted into a CSV file.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-wasteland-data-scrubber` directory and build the Docker image:

```bash
docker build -t wasteland-data-scrubber src/
```

### 2. Prepare Input Data

Create a directory for your input files (e.g., `my_wasteland_data`) and place your raw data logs inside it. For example, `my_wasteland_data/sensor_log.txt`:

```
Sensor Log 234:
[ERROR] Corrupted signal detected.
DATA: [RESOURCE:Water] Amount: 10 units. Location: (COORD:34.56,-118.23)
Noise: asdfasdfasdf
DATA: [RESOURCE:Food] Amount: 5 rations. Location: (COORD:34.57,-118.24)
[WARNING] Battery low.
DATA: [RESOURCE:Scrap Metal] Amount: 15 kg. Location: (COORD:34.58,-118.25)
```

### 3. Run the Scrubber Container

Execute the Docker container, mounting your input and output directories. The scrubber will read from the mounted input path and write the cleaned CSV to the mounted output path.

```bash
mkdir -p my_wasteland_output
docker run --rm \
  -v "$(pwd)/my_wasteland_data:/input" \
  -v "$(pwd)/my_wasteland_output:/output" \
  wasteland-data-scrubber \
  --input /input/sensor_log.txt \
  --output /output/cleaned_resources.csv
```

After execution, `my_wasteland_output/cleaned_resources.csv` will contain the scrubbed data:

```csv
Resource,Amount,Location
Water,10,34.56,-118.23
Food,5,34.57,-118.24
Scrap Metal,15,34.58,-118.25
```

## Development

The core logic resides in `src/scrubber.py`, which is a Python script. The `src/entrypoint.sh` script acts as the container's entry point, parsing arguments and invoking the Python scrubber.

## Tests

To run the automated tests, execute the `tests/test_scrubber.sh` script. This script builds the Docker image, creates mock input and expected output files, runs the container, and verifies the output against the expected results.

```bash
bash tests/test_scrubber.sh
```
