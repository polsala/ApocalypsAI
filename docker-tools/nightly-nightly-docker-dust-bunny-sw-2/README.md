# Nightly Docker Dust Bunny Sweeper

## 🧹 What is this?

The Nightly Docker Dust Bunny Sweeper is a whimsical utility designed to help you keep your Docker environment sparkling clean! It identifies those forgotten, unused digital artifacts – dangling images, orphaned volumes, and lonely networks – that accumulate over time, much like dust bunnies under your bed. While it won't clean them up automatically (yet!), it provides a cheerful report on what it finds, helping you decide what to sweep away.

## ✨ Features

*   **Image Inspection**: Detects dangling Docker images (those not associated with any tagged container).
*   **Volume Vigilance**: Spots unused Docker volumes that are taking up space.
*   **Network Nanny**: Identifies networks that aren't currently attached to any running containers (using Docker's prune logic).
*   **Whimsical Reporting**: Presents its findings with a touch of charm.

## 🚀 How to Use

1.  **Build the Sweeper**: Navigate to the utility's directory and build the Docker image.
    ```bash
    docker build -t docker-dust-bunny-sweeper .
    ```

2.  **Run the Sweeper**: To let the sweeper inspect your Docker environment, you need to mount the Docker socket. This allows the containerized script to interact with your host's Docker daemon.
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker-dust-bunny-sweeper
    ```

    The output will be a report detailing any "dust bunnies" found.

## 🛠️ Development & Testing

### Prerequisites

*   Docker installed and running.
*   Bash shell.

### Running Tests

The tests for the Dust Bunny Sweeper use a mocked `docker` command to ensure determinism and offline execution. This means you don't need a live Docker daemon to run the tests.

1.  Navigate to the utility's directory.
2.  Run the test script:
    ```bash
    bash tests/test_sweeper.sh
    ```

    The tests will simulate various Docker environments (empty, with dangling images, etc.) and verify the sweeper's output.

## 💖 Contributing

Got an idea for a new type of digital dust bunny to sweep? Or a more charming way to report findings? Feel free to contribute!
