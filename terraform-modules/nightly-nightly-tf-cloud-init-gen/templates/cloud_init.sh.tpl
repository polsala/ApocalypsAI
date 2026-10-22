#cloud-config
#cloud-config
# Server Name: ${server_name}

runcmd:
  - echo "Bootstrapping server: ${server_name}"
  ${indent(2, var.boot_script)}
  - echo "Bootstrapping complete for ${server_name}."
