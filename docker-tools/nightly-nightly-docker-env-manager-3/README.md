## Nightly Docker Env Manager

A whimsical yet practical Docker-based utility to spin up and manage isolated development environments. Think of it as your personal digital sandbox, complete with a touch of post-apocalyptic charm.

### Features

*   **Isolation**: Each environment runs in its own container, preventing dependency conflicts.
*   **Reproducibility**: Define your environment using a simple `docker-compose.yml`.
*   **Whimsical Names**: Environments are given fun, survival-themed names.
*   **Easy Management**: Start, stop, and list your environments with simple commands.

### Usage

1.  **Build the Docker Image**: 
    ```bash
    docker build -t apocalypsai/env-manager .
    ```

2.  **Create an Environment Definition**: 
    Create a `my-project-env.yml` file (e.g., `my-dev-env.yml`) in your project directory. This file should be a standard `docker-compose.yml` defining your development services.

    Example `my-dev-env.yml`:
    ```yaml
    version: '3.8'
    services:
      web:
        image: nginx:latest
        ports:
          - "8080:80"
      db:
        image: postgres:14
        environment:
          POSTGRES_USER: user
          POSTGRES_PASSWORD: password
          POSTGRES_DB: mydb
    ```

3.  **Run the Manager**: 
    Use the `docker run` command to interact with the manager. The manager will mount your current directory, allowing it to find your `.yml` definition.

    *   **Start an environment**: 
        ```bash
        docker run --rm -v $(pwd):/app apocalypsai/env-manager start my-dev-env.yml
        ```
        This will start your environment and assign it a random whimsical name (e.g., `wasteland-workbench`, `bunker-builder`).

    *   **List running environments**: 
        ```bash
        docker run --rm -v $(pwd):/app apocalypsai/env-manager list
        ```

    *   **Stop an environment**: 
        ```bash
        docker run --rm -v $(pwd):/app apocalypsai/env-manager stop <environment_name>
        ```
        (Replace `<environment_name>` with the name shown by `list`)

    *   **Stop all environments**: 
        ```bash
        docker run --rm -v $(pwd):/app apocalypsai/env-manager stop-all
        ```

### Development

*   The manager uses a simple Python script to orchestrate `docker-compose` commands.
*   Whimsical names are generated from a predefined list of post-apocalyptic themes.

### Testing

Run tests using `docker-compose run --rm app pytest` within the `docker-tools/nightly-docker-env-manager` directory.
