# Nightly Ansible Data Hoarder

## Summary
This Ansible playbook, `nightly-ansible-data-hoarder`, is designed to help you prepare for the digital apocalypse by ensuring your most precious data is regularly archived and safely transferred to a designated 'hoard' location. Think of it as a digital squirrel preparing for winter, meticulously stashing away nuts (your data) in a secure, remote bunker.

## Whimsical Purpose
In an age where digital bits can vanish faster than a forgotten password, the Data Hoarder ensures your critical files, configurations, and cherished cat memes are preserved. It's your personal digital time capsule, ready to be unearthed when the data streams run dry.

## Usage

1.  **Prerequisites**:
    *   Ansible installed on your control machine.
    *   SSH access (with appropriate keys or password) to the target machine(s) where the source data resides and where the remote hoard path is accessible (can be the same machine).

2.  **Configuration**:
    *   **`src/inventory.ini`**: Define your target hosts. For local execution, `localhost` is sufficient.
        ```ini
        [hoard_targets]
        localhost ansible_connection=local
        # Or for remote hosts:
        # my_server_1 ansible_host=192.168.1.100 ansible_user=your_user
        ```
    *   **`src/vars/hoarding_config.yml`**: This file specifies which directories to archive and where to send them.
        ```yaml
        # src/vars/hoarding_config.yml
        source_dirs:
          - /path/to/your/first/precious/data
          - /path/to/your/second/important/folder
        
        remote_hoard_path: /mnt/remote_backup_drive/digital_bunker
        # Ensure this path exists and is writable by the Ansible user on the target host.
        ```

3.  **Run the Playbook**:
    Execute the playbook from the root of this utility's directory:
    ```bash
    ansible-playbook -i src/inventory.ini src/hoard_data.yml
    ```

    *   The playbook will create a timestamped `.tar.gz` archive for each `source_dir`.
    *   These archives will then be copied to the `remote_hoard_path`.

## How it Works

*   It iterates through the `source_dirs` defined in `hoarding_config.yml`.
*   For each directory, it generates a unique archive name using the current timestamp.
*   It uses `ansible.builtin.archive` to compress the directory on the target host.
*   It then uses `ansible.builtin.copy` to transfer the compressed archive from its temporary location on the target host to the `remote_hoard_path` on the same target host.
*   The playbook is designed to be idempotent for the creation of the remote hoard path, but will always create a new timestamped archive for each run, ensuring a historical record of your data.

## Testing

To ensure your digital hoarding strategy is sound, run the provided test playbook:

```bash
ansible-playbook -i src/inventory.ini tests/test_hoard_data.yml
```

This test playbook will:
1.  Create dummy source directories and files.
2.  Define a temporary local directory to act as the 'remote hoard'.
3.  Execute the `hoard_data.yml` playbook against these dummy paths.
4.  Verify that the expected timestamped archives are created in the temporary 'remote hoard' directory.
5.  Clean up all dummy data and directories.
