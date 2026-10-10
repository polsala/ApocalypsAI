# Nightly Ansible Serenity Scroll Deployer

This Ansible playbook, `nightly-ansible-serenity-scrol`, brings a touch of digital zen to your servers by deploying whimsical "serenity scrolls." These are simple text files containing uplifting messages, ASCII art, or gentle reminders, placed in a designated directory on your target machines. The playbook can be configured to rotate these scrolls, ensuring a fresh dose of tranquility with each run.

## Features

*   **Whimsical Deployment:** Places a randomly selected "serenity scroll" on your servers.
*   **Configurable Path:** Easily change where the scrolls are deployed.
*   **Simple Rotation:** Future enhancements could include rotation logic to cycle through scrolls. (For now, it deploys one, and subsequent runs will replace it if `force` is true, or do nothing if the same scroll is already there).
*   **Idempotent:** Running the playbook multiple times will result in the same state unless variables change.

## Usage

### Prerequisites

*   Ansible installed on your control machine.
*   SSH access to your target servers (or `--connection=local` for local testing).

### Files

*   `src/deploy_serenity_scroll.yml`: The main Ansible playbook.
*   `src/inventory.ini`: An example inventory file.
*   `src/vars/main.yml`: Defines variables like the target directory and available scroll templates.
*   `src/templates/scroll_01.j2`, `src/templates/scroll_02.j2`, `src/templates/scroll_03.j2`: Example serenity scroll templates.

### Running the Playbook

1.  **Define your inventory:** Edit `src/inventory.ini` to include your target servers. For local testing, you can use `localhost`.

    ```ini
    [servers]
    localhost ansible_connection=local
    # your_server_ip
    ```

2.  **Customize variables (optional):** Modify `src/vars/main.yml` if you want to change the `serenity_scroll_dir` or add more `scroll_templates`.

3.  **Execute the playbook:**

    ```bash
    ansible-playbook -i src/inventory.ini src/deploy_serenity_scroll.yml
    ```

    After running, check the `{{ serenity_scroll_dir }}` on your target server(s) for the deployed scroll!

## Testing

The utility includes a self-contained test playbook that verifies the deployment process.

### Running Tests

```bash
ansible-playbook -i src/inventory.ini tests/test_deploy_serenity_scroll.yml
```

This test playbook will:
1.  Run the main `deploy_serenity_scroll.yml` playbook's tasks.
2.  Verify that the target directory exists.
3.  Verify that a scroll file has been deployed.
4.  Read the content of the deployed scroll and assert that it matches one of the expected template contents.

**Mock rationale:** The tests use `ansible.builtin.stat` and `ansible.builtin.slurp` modules, which operate directly on the local filesystem when `--connection=local` is used. This makes them deterministic and offline. The randomness of scroll selection is handled by asserting that the deployed content matches *any* of the predefined scroll templates, rather than a specific one. A cleanup task ensures the test environment is reset after each run, guaranteeing determinism.
