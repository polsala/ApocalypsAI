# Nightly Container Compost Heap

## 🌿 Overview

The `nightly-container-compost-heap` is a whimsical yet powerful utility designed to help you maintain a clean and efficient Docker environment. In the post-apocalyptic digital wasteland, every byte of storage is precious. This tool helps you "compost" your digital detritus – unused Docker containers, dangling images, and orphaned volumes – turning them into fresh, reclaimable space for new growth in your container garden.

Think of it as a friendly digital gardener, tidying up the overgrown patches of your system.

## ✨ Features

*   **Whimsical Output**: Enjoy delightful messages as your digital waste is transformed.
*   **Deep Cleaning**: Prunes all stopped containers, dangling images, and unused networks and volumes.
*   **Dry Run Mode**: See what would be composted before committing to the cleanup, ensuring no precious digital flora is accidentally removed.
*   **Containerized**: Designed as a `docker-tools` utility, it's self-contained and easy to run.

## 🚀 Usage

### Prerequisites

*   Docker must be installed and running on your system.
*   The user running the script must have permissions to interact with the Docker daemon (e.g., be part of the `docker` group or run with `sudo`).

### Running the Compost Heap

1.  **Clone the repository (or navigate to the utility's directory):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/docker-tools/nightly-container-compost-heap
    ```

2.  **Make the script executable:**
    ```bash
    chmod +x src/compost.sh
    ```

3.  **Perform a Dry Run (Recommended First!):**
    See what digital waste is available for composting without actually removing anything.
    ```bash
    ./src/compost.sh --dry-run
    ```
    This will show you an estimate of the space that could be reclaimed.

4.  **Initiate the Composting Process:**
    Once you're satisfied with the dry run, unleash the full power of the Compost Heap!
    ```bash
    ./src/compost.sh
    ```
    This command will execute `docker system prune --force --volumes`, removing:
    *   All stopped containers
    *   All dangling images (images not associated with any container)
    *   All unused networks
    *   All unused volumes

    You will see a summary of the reclaimed space.

## 🧪 Testing

To ensure the Digital Compost Heap is working as intended without affecting your actual Docker environment, you can run the provided tests. These tests use a mocked `docker` command to simulate its behavior.

1.  **Make the test script executable:**
    ```bash
    chmod +x tests/test_compost.sh
    ```

2.  **Run the tests:**
    ```bash
    ./tests/test_compost.sh
    ```
    You should see output indicating whether each test passed or failed.
