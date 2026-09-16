# Nightly Mind Moss Cultivator

## Summary

This Ansible playbook helps you cultivate your personal digital garden by automating the deployment of a static site generator (Zola) and Nginx web server on a remote Linux server. It sets up the necessary directories, installs dependencies, configures Nginx, and gets your 'mind moss' ready to grow!

## Whimsical Purpose

In the post-apocalyptic landscape, clarity of thought and the preservation of knowledge are paramount. The 'Mind Moss Cultivator' ensures your precious thoughts, notes, and insights have a fertile digital ground to flourish, accessible even when the world outside is chaotic. It's your personal sanctuary for ideas, a quiet corner of the internet where your wisdom can take root and spread.

## Prerequisites

*   **Ansible**: Installed on your control machine.
*   **Remote Server**: A Debian-based Linux server (e.g., Ubuntu) with `sudo` access for the Ansible user.
*   **SSH Access**: Your Ansible control machine must have SSH access to the remote server.
*   **Domain Name (Optional but Recommended)**: A domain name pointed to your server's IP address if you want to access your garden via a custom URL.

## Usage

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/ansible-playbooks/nightly-mind-moss-cultivator
    ```

2.  **Configure your inventory**: Edit `src/inventory.ini` to include your remote server(s).

    ```ini
    # src/inventory.ini
    [webservers]
    your_server_ip_or_hostname ansible_user=your_ssh_user
    ```

3.  **Customize variables**: Edit `src/vars/main.yml` to define your digital garden's settings.

    ```yaml
    # src/vars/main.yml
    site_name: my_digital_garden
    domain: example.com # Your domain, or leave as IP if not using one
    zola_version: 0.17.2
    # Zola URL and checksum are pre-filled for v0.17.2, update if changing version
    zola_url: "https://github.com/getzola/zola/releases/download/v{{ zola_version }}/zola-v{{ zola_version }}-x86_64-unknown-linux-gnu.tar.gz"
    zola_checksum: "sha256:647185078519e49635955030283c4193568853610e7403487002061301389025"
    nginx_conf_path: /etc/nginx/sites-available/{{ site_name }}.conf
    nginx_site_enabled_path: /etc/nginx/sites-enabled/{{ site_name }}.conf
    ```

4.  **Run the playbook**: Execute the playbook from the `nightly-mind-moss-cultivator` directory.

    ```bash
    ansible-playbook -i src/inventory.ini src/cultivate_garden.yml
    ```

5.  **Start cultivating!**
    After the playbook runs, Zola will be installed, Nginx configured, and a basic site structure created at `/var/www/{{ site_name }}` on your remote server. You can then `ssh` into your server, navigate to this directory, and start adding content to the `content/` folder. Remember to run `zola build` in the site root to generate the static files, and Nginx will serve them.

## Testing

To run the self-contained, offline tests for this playbook:

```bash
ansible-playbook -i tests/test_inventory.ini tests/test_cultivate_garden.yml
```

This test playbook uses `connection: local` and `gather_facts: no` to simulate a target environment by explicitly defining `ansible_facts` and other variables. It then uses `assert` to verify that key variables are correctly defined and that the playbook's logic would process them as expected, without making any actual changes to your system or requiring a remote connection.
