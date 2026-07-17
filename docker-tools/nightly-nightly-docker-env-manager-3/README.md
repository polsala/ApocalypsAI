## Nightly Docker Env Manager

A whimsical yet practical utility for managing isolated development environments using Docker. This tool allows you to define, create, start, stop, and destroy development environments based on simple YAML configurations.

### Philosophy

Embrace the chaos of development with the discipline of containerization. This tool aims to provide a quick and reproducible way to spin up temporary workspaces, ensuring your main system remains pristine.

### Features

*   **Environment Definitions**: Define your development environments (e.g., Python, Node.js, Go) in a `docker-compose.yml` format.
*   **Container Management**: Easily start, stop, and restart your defined environments.
*   **Isolation**: Keep your development dependencies separate from your host system.
*   **Clean Slate**: Destroy environments completely when done, leaving no trace.

### Usage

1.  **Prerequisites**: Ensure you have Docker and Docker Compose installed on your system.

2.  **Configuration**: Create a `env.yaml` file in the root directory of your project to define your environment. See `example_env.yaml` for an example.

    ```yaml
    # example_env.yaml
    name: my-python-dev
    services:
      python_app:
        build:
          context: .
          dockerfile: Dockerfile.python
        volumes:
          - .:/app
        ports:
          - "8000:8000"
        command: "python app.py"
    ```

3.  **Dockerfile**: Create a `Dockerfile.python` (or similar, based on your `env.yaml` definition) in the same directory.

    ```dockerfile
    # Dockerfile.python
    FROM python:3.9-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    ```

4.  **Run Commands**: Use the `docker-env-manager` script (built into the container) to manage your environment.

    *   **Start an environment**: `docker-env-manager start`
    *   **Stop an environment**: `docker-env-manager stop`
    *   **Restart an environment**: `docker-env-manager restart`
    *   **Destroy an environment**: `docker-env-manager destroy`
    *   **View status**: `docker-env-manager status`

### Building the Docker Image

```bash
docker build -t apoc-env-manager .
```

### Running the Manager

Once the image is built, you can run it and mount your project directory to manage its environment.

```bash
docker run -it --rm -v $(pwd):/app -v /var/run/docker.sock:/var/run/docker.sock apoc-env-manager start
```

(Replace `start` with `stop`, `restart`, or `destroy` as needed.)

### Testing

Run the tests using `docker-compose run --rm tester` after building the image.
