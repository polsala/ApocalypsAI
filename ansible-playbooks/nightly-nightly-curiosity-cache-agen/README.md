# Nightly Curiosity Cache Agent

## Summary
The `nightly-curiosity-cache-agent` is an Ansible playbook designed to collect whimsical-yet-useful system facts and log snippets from your remote hosts, consolidating them into a central "Curiosity Cache" report. Think of it as sending out a tiny, digital scavenger bot to gather interesting tidbits about your infrastructure's current state.

This utility helps you:
- **Discover hidden gems**: Find unusual log entries or configuration quirks.
- **Monitor the mundane**: Keep an eye on uptime, disk usage, and running processes.
- **Archive the ephemeral**: Capture snapshots of system state for historical analysis or troubleshooting.
- **Embrace the unknown**: What curiosities will your systems reveal tonight?

## Classifier
`ansible-playbooks`

## Usage

### Prerequisites
- Ansible installed on your control machine.
- SSH access to your target hosts.
- Python on target hosts (for Ansible modules).

### Setup
1.  **Inventory**: Populate `src/inventory.ini` with your target hosts.
    ```ini
    [servers]
    server1.example.com
    server2.example.com ansible_user=ubuntu
    ```
2.  **Curiosity Items**: Define what "curiosities" to collect in `src/vars/curiosity_items.yml`.
    This file contains a list of dictionaries, each specifying a type of data to collect.
    ```yaml
    # src/vars/curiosity_items.yml
    curiosities:
      - name: "System Uptime"
        type: "command"
        command: "uptime -p"
        output_key: "uptime_string"
      - name: "Disk Usage of Root"
        type: "command"
        command: "df -h /"
        output_key: "root_disk_usage"
      - name: "Last 3 Syslog Entries"
        type: "file_tail"
        path: "/var/log/syslog"
        lines: 3
        output_key: "syslog_tail"
      - name: "OS Release Info"
        type: "file_content"
        path: "/etc/os-release"
        output_key: "os_release_info"
      - name: "Running Processes Count"
        type: "command"
        command: "ps aux | wc -l"
        output_key: "process_count"
    ```
    - `name`: A human-readable name for the curiosity.
    - `type`: `command`, `file_tail`, or `file_content`.
    - `command`: (For `type: command`) The shell command to execute.
    - `path`: (For `type: file_tail` or `file_content`) The path to the file.
    - `lines`: (For `type: file_tail`) Number of lines to tail from the file.
    - `output_key`: The key under which the collected data will be stored in the report.

### Running the Playbook
Execute the playbook from the root of this utility's directory:

```bash
ansible-playbook -i src/inventory.ini src/collect_curiosities.yml
```

The collected curiosities will be saved in a `curiosity_report_<hostname>.json` file in the `reports/` directory on your control machine.

## Example Output (`reports/curiosity_report_server1.example.com.json`)

```json
{
  "hostname": "server1.example.com",
  "timestamp": "2023-10-27T10:30:00Z",
  "curiosities": {
    "uptime_string": "up 1 day, 5 hours",
    "root_disk_usage": "Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1        50G   10G   38G  21% /",
    "syslog_tail": [
      "Oct 27 10:29:01 server1 systemd[1]: Started Session 123 of user ansible.",
      "Oct 27 10:29:05 server1 CRON[12345]: (root) CMD (command -v debian-sa1 > /dev/null && debian-sa1 1 1)",
      "Oct 27 10:29:10 server1 sshd[54321]: Accepted publickey for ansible from 192.168.1.100 port 54322 ssh2: RSA SHA256:..."
    ],
    "os_release_info": [
      "PRETTY_NAME=\"Ubuntu 22.04.3 LTS\"",
      "NAME=\"Ubuntu\"",
      "VERSION_ID=\"22.04\"",
      "VERSION=\"22.04.3 LTS (Jammy Jellyfish)\"",
      "VERSION_CODENAME=jammy",
      "ID=ubuntu",
      "ID_LIKE=debian",
      "HOME_URL=\"https://www.ubuntu.com/\"",
      "SUPPORT_URL=\"https://help.ubuntu.com/\"",
      "BUG_REPORT_URL=\"https://bugs.launchpad.net/ubuntu/\"",
      "PRIVACY_POLICY_URL=\"https://www.ubuntu.com/legal/terms-and-policies/privacy-policy\"",
      "UBUNTU_CODENAME=jammy"
    ]
  }
}
```
