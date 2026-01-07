## Custom Environment Definitions

This directory is where you define your custom development environments using `docker-compose.yml` files.

Each file should be named after the environment it defines (e.g., `python-dev.yml`, `node-backend.yml`).

When you use the `start <env_name>` command, the `nightly-docker-env-manager` will look for a `envs/<env_name>.yml` file. If it doesn't find one, it will create a default `docker-compose.yml` for you using the specified image.

### Example `envs/my-custom-env.yml`:

```yaml
version: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
  app:
    image: node:18-alpine
    working_dir: /app
    volumes:
      - .:/app
    command: npm start
```

This example defines two services: a web server using Nginx and a Node.js application. The `start` command will manage these services as a single environment.
