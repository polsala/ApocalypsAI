#!/usr/bin/env bash\n\nset -e\n\n# Ensure we are in the module directory\nSCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)\ncd "$SCRIPT_DIR/.."\n\n# Initialize Terraform with a local (no‑backend) configuration\nterraform init -backend=false > /dev/null\n\n# Validate the configuration syntax\nterraform validate\n\n# Perform a dry‑run plan with mock variable values\nterraform plan -input=false \\
  -var 'bucket_name=test-safehouse-bucket' \\
  -var 'allowed_role_name=test-role' > /dev/null\n\necho "All tests passed."
