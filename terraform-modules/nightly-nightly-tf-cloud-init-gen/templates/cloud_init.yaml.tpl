#cloud-config

# Whimsical Banner
runcmd:
  - |-
    echo "=================================================="
    echo "  ${banner_message}"
    echo "  Instance: ${instance_name}"
    echo "=================================================="

# Install packages if provided
{% if package_list %}
packages:
{% for pkg in package_list %}
  - {{ pkg }}
{% endfor %}
{% endif %}

# Execute custom script if provided
{% if user_data_script %}
runcmd:
  - |-
    {{ user_data_script }}
{% endif %}
