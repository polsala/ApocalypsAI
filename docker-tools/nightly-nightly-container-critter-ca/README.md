# Nightly Container Critter Caretaker

## Summary
The `nightly-container-critter-care` utility provides a whimsical yet practical way to manage small, isolated Docker containers that act as 'digital critters'. Each critter has a 'mood' that can be influenced by interactions, demonstrating basic Docker Compose usage, container lifecycle management, and inter-container communication patterns.

## How it Works
This utility uses `docker-compose` to define and manage individual 'critter' containers. Each critter is a simple Python application running inside its own container. The Python script maintains a 'mood' state in a file, which can be updated by sending commands to the container via `docker-compose exec`.

### Core Components:
*   `critter_manager.sh`: A bash script to initialize, start, stop, check status, and interact with your critters.
*   `critter_template/Dockerfile`: Defines the Docker image for a generic critter.
*   `critter_template/critter.py`: The Python application that runs inside each critter container, managing its mood.
*   `docker-compose.yml` (generated): A Docker Compose file created for each critter, linking its local files to the container.

## Requirements
*   Docker (daemon and CLI)
*   Docker Compose
*   Bash shell

## Setup
No special setup is required beyond having Docker and Docker Compose installed. The utility will create a `critters/` directory in its working location to store your critter configurations.

## Usage
Navigate to the `nightly-container-critter-care` directory and use the `critter_manager.sh` script.

### Commands:
*   `./src/critter_manager.sh init <critter_name>`: Initializes a new critter with the given name. This creates a directory for the critter, copies the template files, and generates a `docker-compose.yml`.
*   `./src/critter_manager.sh start <critter_name>`: Starts the specified critter container in detached mode.
*   `./src/critter_manager.sh stop <critter_name>`: Stops and removes the specified critter container.
*   `./src/critter_manager.sh status <critter_name>`: Shows the Docker Compose status for the specified critter.
*   `./src/critter_manager.sh interact <critter_name> <command>`: Sends a command to the critter. Supported commands are `feed` and `play`.

### Example Workflow:

1.  **Initialize a new critter**: Let's call it 'Sparky'.
    ```bash
    ./src/critter_manager.sh init Sparky
    ```
    _Output: Critter 'Sparky' initialized._

2.  **Start Sparky**: 
    ```bash
    ./src/critter_manager.sh start Sparky
    ```
    _Output: Starting Sparky-critter-container ... done_

3.  **Check Sparky's status**: 
    ```bash
    ./src/critter_manager.sh status Sparky
    ```
    _Output (example):
    Name                     Command               State    Ports
    -------------------------------------------------------------------
    Sparky-critter-container   python /app/critter.py   Up      
    _

4.  **Interact with Sparky (check mood)**:
    ```bash
    ./src/critter_manager.sh interact Sparky
    ```
    _Output: Critter is feeling Content._

5.  **Feed Sparky**: 
    ```bash
    ./src/critter_manager.sh interact Sparky feed
    ```
    _Output: Critter fed! It's feeling Happy._

6.  **Play with Sparky**: 
    ```bash
    ./src/critter_manager.sh interact Sparky play
    ```
    _Output: Critter played with! It's feeling Excited._

7.  **Stop Sparky**: 
    ```bash
    ./src/critter_manager.sh stop Sparky
    ```
    _Output: Stopping Sparky-critter-container ... done_

This utility provides a fun way to experiment with Docker and Docker Compose in a controlled, interactive environment.
