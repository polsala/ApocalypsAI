#!/usr/bin/env bash\nset -e\n# Mock rationale: Use local backend to avoid cloud calls.\nterraform init -backend=false > /dev/null 2>&1\nterraform validate\necho \"Validation passed.\"\n
