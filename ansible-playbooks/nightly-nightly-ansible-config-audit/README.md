## Nightly Ansible Config Auditor

This utility provides an Ansible playbook designed to audit system configurations against a predefined baseline. It helps identify deviations and ensures systems adhere to desired security and operational standards.

### Purpose

In the chaotic aftermath of an apocalypse, maintaining consistent and secure system configurations is paramount. This playbook automates the process of checking critical configuration files and settings, alerting operators to any drift from the established 'safe' state.

### Features

*   **Configurable Baseline**: Define expected configurations in a separate YAML file.
*   **File Integrity Checks**: Verify checksums of critical files.
*   **Service Status Checks**: Ensure essential services are running.
*   **User/Group Audits**: Check for unauthorized users or group memberships.
*   **Reporting**: Generates a summary report of all audited items and any discrepancies.

### Usage

1.  **Prerequisites**: Ensure Ansible is installed on your control machine.
2.  **Inventory**: Create or update your Ansible inventory file (`inventory.ini`) to include the target hosts.
3.  **Baseline Configuration**: Define your desired system state in `vars/baseline_config.yml`.
4.  **Run the Playbook**: Execute the playbook using the following command:
    ```bash
    ansible-playbook -i inventory.ini audit_config.yml
    ```

### Files

*   `audit_config.yml`: The main Ansible playbook.
*   `inventory.ini`: Example inventory file.
*   `vars/baseline_config.yml`: Defines the expected configuration baseline.
*   `templates/audit_report.j2`: Jinja2 template for generating the audit report.
*   `tests/test_audit_config.yml`: Molecule test for the playbook.
*   `tests/molecule/default/molecule.yml`: Molecule configuration.
*   `tests/molecule/default/converge.yml`: Molecule converge playbook.
*   `tests/molecule/default/verify.yml`: Molecule verify playbook.
