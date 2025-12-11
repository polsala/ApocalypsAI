## Nightly Ansible Config Auditor

This utility provides an Ansible playbook designed to audit system configurations against a defined desired state. It helps identify deviations and provides a report of any discrepancies.

### Purpose

In the chaotic aftermath of an apocalypse, maintaining consistent and secure system configurations is paramount. This playbook acts as a vigilant guardian, ensuring that critical systems adhere to established security baselines and operational standards.

### Usage

1.  **Define your desired state**: Create or modify the `vars/desired_state.yml` file to specify the expected configurations for your systems. This can include package versions, file permissions, service statuses, and more.
2.  **Prepare your inventory**: Ensure your `inventory.ini` file correctly lists the target hosts you wish to audit.
3.  **Run the playbook**: Execute the playbook using the `ansible-playbook` command:
    ```bash
    ansible-playbook -i inventory.ini audit_config.yml
    ```

### Playbook Structure

*   `audit_config.yml`: The main playbook file.
*   `inventory.ini`: An example inventory file.
*   `vars/desired_state.yml`: A variable file defining the desired configuration state.
*   `templates/config_report.j2`: Jinja2 template for generating the audit report.
*   `tests/test_audit_config.yml`: An Ansible playbook for testing the main playbook's logic.
*   `tests/inventory_test.ini`: An inventory file for testing.

### Example `vars/desired_state.yml`

```yaml
desired_packages:
  - name: "openssh-server"
    state: "present"
  - name: "fail2ban"
    state: "present"

desired_services:
  - name: "sshd"
    state: "started"
    enabled: "yes"
  - name: "cron"
    state: "started"
    enabled: "yes"

desired_files:
  - path: "/etc/ssh/sshd_config"
    mode: "0600"
    owner: "root"
    group: "root"
```

### Example `templates/config_report.j2`

```jinja2
--- Configuration Audit Report ---

Host: {{ inventory_hostname }}
Timestamp: {{ ansible_date_time.iso8601 }}

{% if audit_results.packages is defined %}
Package Audits:
{% for pkg in audit_results.packages %}
  - Package: {{ pkg.name }}
    Expected State: {{ pkg.desired_state }}
    Actual State: {{ pkg.state }}
    Status: {{ 'MATCH' if pkg.state == pkg.desired_state else 'MISMATCH' }}
{% endfor %}
{% endif %}

{% if audit_results.services is defined %}
Service Audits:
{% for svc in audit_results.services %}
  - Service: {{ svc.name }}
    Expected State: {{ svc.desired_state }}
    Actual State: {{ svc.state }}
    Expected Enabled: {{ svc.desired_enabled }}
    Actual Enabled: {{ svc.enabled }}
    Status: {{ 'MATCH' if svc.state == svc.desired_state and svc.enabled == svc.desired_enabled else 'MISMATCH' }}
{% endfor %}
{% endif %}

{% if audit_results.files is defined %}
File Audits:
{% for fil in audit_results.files %}
  - File: {{ fil.path }}
    Expected Mode: {{ fil.desired_mode }}
    Actual Mode: {{ fil.mode }}
    Expected Owner: {{ fil.desired_owner }}
    Actual Owner: {{ fil.owner }}
    Expected Group: {{ fil.desired_group }}
    Actual Group: {{ fil.group }}
    Status: {{ 'MATCH' if fil.mode == fil.desired_mode and fil.owner == fil.desired_owner and fil.group == fil.desired_group else 'MISMATCH' }}
{% endfor %}
{% endif %}

--- End of Report ---
