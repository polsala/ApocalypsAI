# Nightly Digital Comfort Zone Enforcer

This Ansible playbook helps you maintain a consistent 'digital comfort zone' across your remote servers. It ensures that specific files (like custom MOTDs, daily affirmations, or `.bash_aliases`) are present, have the correct content, and appropriate permissions.

## Features

- **File Presence & Content**: Guarantees specified files exist with their desired content.
- **Permissions Management**: Sets appropriate file permissions.
- **Directory Creation**: Automatically creates parent directories if they don't exist.
- **Customizable**: Easily define your 'comfort files' and their properties in `vars/comfort_files.yml`.

## Usage

1.  **Define your inventory**: Create an `inventory.ini` file listing your target hosts.
    ```ini
    [servers]
    your_server_1 ansible_host=192.168.1.10
    your_server_2 ansible_host=192.168.1.11

    [all:vars]
    ansible_python_interpreter=/usr/bin/python3
    # You might need to specify ansible_user if it's different from your SSH user
    # ansible_user=your_remote_user
    ```

2.  **Customize comfort files**: Edit `vars/comfort_files.yml` to define the files you want to manage. The `comfort_zone_base_path` variable can be used to prepend a path to all defined file paths, useful for testing or specific deployments.

    ```yaml
    # vars/comfort_files.yml
    comfort_zone_base_path: "" # Set to a path like /tmp/my_comfort_zone for testing, or leave empty for absolute paths.

    comfort_zone_files:
      - path: "/etc/motd.d/apocalypsai_welcome"
        content: "Welcome, Survivor! May your code be bug-free and your coffee strong.\n"
        mode: "0644"
      - path: "/home/{{ ansible_user }}/.config/apocalypsai/daily_affirmation.txt"
        content: "You are resilient. You are creative. You are integrated.\n"
        mode: "0600"
      - path: "/home/{{ ansible_user }}/.bash_aliases"
        content: |-
          alias comfort='echo "Feeling comfy?"'
          alias integrate='ansible-playbook ~/nightly-comfort-zone-enforce/src/comfort_zone.yml'
        mode: "0644"
    ```

3.  **Run the playbook**: Execute the playbook using `ansible-playbook`.

    ```bash
    ansible-playbook -i src/inventory.ini src/comfort_zone.yml --ask-become-pass
    ```
    (Use `--ask-become-pass` if `become: yes` is required and you don't have passwordless sudo configured).

## Testing

To run the automated tests, ensure you have Ansible installed and then execute:

```bash
ansible-playbook -i tests/inventory_test.ini tests/test_comfort_zone.yml --ask-become-pass
```

This will create a temporary directory in your home folder (`~/.ansible_test_comfort_zone`), apply the comfort zone files there, verify their content and permissions, and then clean up. The `ansible_user` variable in `vars/comfort_files.yml` will resolve to your current user during testing.
