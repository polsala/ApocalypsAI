## Nightly Docker Env Manager

A whimsical yet useful utility for managing isolated Dockerized development environments. This tool allows you to quickly spin up, tear down, and list your ephemeral development environments, ensuring a clean workspace for every project.

### Philosophy

Embrace the chaos of development with the discipline of containerization. This tool aims to provide a simple, repeatable, and isolated way to manage your dev environments, preventing dependency conflicts and keeping your host system clean.

### Usage

1.  **Build the Docker image:**
    ```bash
    docker build -t apoc-env-manager .
    ```

2.  **Run the manager:**
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apoc-env-manager <command>
    ```

    Replace `<command>` with one of the following:

    *   `up <env_name> <dockerfile_path>`: Starts a new environment from a Dockerfile. The `dockerfile_path` should be a path to a directory containing a `Dockerfile`.
    *   `down <env_name>`: Stops and removes a running environment.
    *   `list`: Lists all currently running managed environments.
    *   `logs <env_name>`: Shows the logs for a specific environment.

### Example

Let's say you have a project in `./my-app` with a `Dockerfile` inside.

1.  **Start the environment:**
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apoc-env-manager up my-app-env ./my-app
    ```

2.  **List environments:**
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apoc-env-manager list
    ```

3.  **Stop the environment:**
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apoc-env-manager down my-app-env
    ```

### Contributing

Feel free to fork this repository and submit pull requests. New features, bug fixes, and improvements are always welcome!
