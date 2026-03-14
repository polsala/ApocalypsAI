# Nightly Survival Kit Dockerizer

## Summary
This utility helps you prepare for the inevitable by whimsically suggesting relevant containerized tools (Docker images) for items in your survival kit. Simply provide a text file listing your essential items, and the `Survival Kit Dockerizer` will output a list of corresponding survival functions and hypothetical Docker images that could assist you in a post-apocalyptic world.

It's a fun way to think about digital preparedness for physical survival!

## How it Works
The tool reads each line from your input file, identifies key survival items, and maps them to a 'survival function' and a suggested (hypothetical) Docker image. The core logic is embedded within a Python script inside a Docker container.

## Usage

### 1. Create your survival kit list
Create a file, for example, `my_kit.txt`, with one item per line:

```
water filter
first aid kit
radio
seeds
flashlight
knife
map
compass
fire starter
rope
canned food
books
```

### 2. Build the Docker image
Navigate to the `nightly-survival-kit-dockerizer` directory (or the directory containing the `Dockerfile` and `src` folder) and build the Docker image:

```bash
docker build -t apocalypsai/survival-kit-dockerizer:latest .
```

### 3. Run the utility
Mount your `my_kit.txt` file into the container at `/app/kit.txt` and run the image. The utility expects the path to the kit file as its first argument.

```bash
docker run --rm -v "$(pwd)/my_kit.txt:/app/kit.txt" apocalypsai/survival-kit-dockerizer:latest /app/kit.txt
```

Replace `my_kit.txt` with the actual path to your survival kit file.

### Example Output
```
Processing survival kit...

Item: water filter
  Survival Function: Hydration Management
  Suggested Docker Tool: apocalypsai/aqua-purifier-bot:latest

Item: first aid kit
  Survival Function: Emergency Medicine
  Suggested Docker Tool: apocalypsai/med-scanner-cli:latest

Item: radio
  Survival Function: Long-Range Comms
  Suggested Docker Tool: apocalypsai/signal-scout-cli:latest

Item: seeds
  Survival Function: Sustainable Agriculture
  Suggested Docker Tool: apocalypsai/terra-cultivator-ai:latest

...
```

## Development
The core logic is a simple Python script (`src/survival_kit_dockerizer.py`) that contains a hardcoded mapping of keywords to survival functions and suggested Docker images. The `Dockerfile` sets up the environment and runs this script.
