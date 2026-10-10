#cloud-config

# Set a randomized MOTD
runcmd:
  - echo "Welcome to the ${instance_name}! Your secret handshake command is: ${secret_command}" > /etc/motd
  - echo "# Generated MOTD seed: ${random_motd_seed}" >> /etc/motd

  # Install and configure ufw
  - apt-get update -y
  - apt-get install -y ufw
  - ufw --force enable
  - ufw allow ${ssh_port}/tcp
  - ufw allow ${secret_port}/tcp
  - ufw default deny incoming
  - ufw default allow outgoing

  # Create admin user with randomized password (for demonstration, use proper secrets management in production)
  - useradd -m -s /bin/bash ${admin_user}
  - echo "${admin_user}:${admin_password}" | chpasswd
  - echo "${admin_user} ALL=(ALL) NOPASSWD: ALL" | tee /etc/sudoers.d/${admin_user}
  - chmod 0440 /etc/sudoers.d/${admin_user}

  # Add a 'secret handshake' command that reveals a hidden message
  - echo "#!/bin/bash\nif [ \"$1\" = \"${secret_command}\" ]; then\n  echo \"You found the secret! The true apocalypse is... still coming.\"\nelse\n  echo \"Invalid handshake. Try again, survivor.\"\nfi" > /usr/local/bin/secret_handshake
  - chmod +x /usr/local/bin/secret_handshake
