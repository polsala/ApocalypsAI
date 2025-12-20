Nightly Ansible Docker Compose Deployer

Overview:
This utility provides an Ansible playbook that installs Docker, deploys a Docker Compose stack, and performs basic health checks on the services.

Usage:
ansible-playbook -i inventory.ini deploy.yml --extra-vars "compose_path=./docker-compose.yml"

The playbook works with Debian-based systems (apt). Adjust tasks for other OS families as needed.

Structure:
- inventory.ini – simple local inventory
- deploy.yml – main playbook
- tests/ – unit tests that mock ansible execution
