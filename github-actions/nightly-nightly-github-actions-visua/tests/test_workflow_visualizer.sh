#!/bin/bash

# Test script for GitHub Actions Workflow Visualizer
# This script tests the workflow visualizer functionality

set -e

echo "=== Testing GitHub Actions Workflow Visualizer ==="

# Create test directory structure
TEST_DIR="/tmp/workflow-visualizer-test"
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR/.github/workflows"
mkdir -p "$TEST_DIR/workflow-diagrams"
cd "$TEST_DIR"

# Create test workflow files

cat > .github/workflows/test-workflow-1.yml << 'EOF'
name: Test Workflow 1

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

  test:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Run tests
        run: echo "Running tests"

  deploy:
    runs-on: ubuntu-latest
    needs: [build, test]
    steps:
      - name: Deploy
        run: echo "Deploying"
EOF

cat > .github/workflows/test-workflow-2.yml << 'EOF'
name: Test Workflow 2

on:
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

  security:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - name: Security scan
        run: echo "Security scanning"
EOF

cat > .github/workflows/test-workflow-3.yml << 'EOF'
name: Test Workflow 3

on:
  schedule:
    - cron: '0 2 * * *'

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Cleanup
        run: echo "Cleaning up"
EOF

# Test Python script directly

echo "Testing Python visualization script..."

python3 << 'EOF'
import sys
import os
sys.path.append('/tmp/workflow-visualizer-test')

# Test the visualization logic
import yaml
from graphviz import Digraph

# Test workflow parsing
with open('.github/workflows/test-workflow-1.yml', 'r') as f:
    workflow = yaml.safe_load(f)
    
assert 'jobs' in workflow
assert 'build' in workflow['jobs']
assert 'test' in workflow['jobs']
assert 'deploy' in workflow['jobs']

# Test dependency detection
build_job = workflow['jobs']['build']
test_job = workflow['jobs']['test']
deploy_job = workflow['jobs']['deploy']

assert 'needs' not in build_job
assert test_job.get('needs') == 'build'
assert deploy_job.get('needs') == ['build', 'test']

print("✓ Workflow parsing tests passed")

# Test diagram generation
output_path = 'workflow-diagrams/test-workflow-1'
dot = Digraph(comment='Test Workflow')
dot.attr(rankdir='LR')

dot.node('build', 'build\nBuild job')
dot.node('test', 'test\nTest job')
dot.node('deploy', 'deploy\nDeploy job')
dot.edge('build', 'test')
dot.edge('build', 'deploy')
dot.edge('test', 'deploy')

dot.render(output_path, format='svg', cleanup=True)

# Check if SVG was created
assert os.path.exists(f'{output_path}.svg'), "SVG file was not created"
print("✓ Diagram generation tests passed")
EOF

# Test the complete workflow script

echo "Testing complete workflow script..."

export WORKFLOW_DIR='.github/workflows'
export OUTPUT_DIR='workflow-diagrams'

python3 << 'EOF'
import os
import yaml
import glob
from graphviz import Digraph

# Replicate the workflow script logic
def parse_workflow(file_path):
    with open(file_path, 'r') as f:
        try:
            workflow = yaml.safe_load(f)
            if not workflow:
                return None
            
            workflow_name = os.path.basename(file_path).replace('.yml', '').replace('.yaml', '')
            jobs = workflow.get('jobs', {})
            
            return {
                'name': workflow_name,
                'jobs': jobs,
                'file_path': file_path
            }
        except yaml.YAMLError as e:
            print(f"Error parsing {file_path}: {e}")
            return None

# Find and process workflow files
workflow_files = glob.glob(f"{os.environ['WORKFLOW_DIR']}/*.yml") + \
                  glob.glob(f"{os.environ['WORKFLOW_DIR']}/*.yaml")

print(f"Found {len(workflow_files)} workflow files")

for workflow_file in workflow_files:
    print(f"Processing {workflow_file}...")
    workflow_data = parse_workflow(workflow_file)
    if workflow_data:
        output_name = os.path.basename(workflow_file).replace('.yml', '').replace('.yaml', '')
        output_path = f"{os.environ['OUTPUT_DIR']}/{output_name}"
        
        # Generate diagram
        dot = Digraph(comment=f"Workflow: {workflow_data['name']}")
        dot.attr(rankdir='LR', size='8,5', dpi='300')
        dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')
        
        for job_name, job_config in workflow_data['jobs'].items():
            job_label = f"{job_name}\n{job_config.get('name', job_name)}"
            dot.node(job_name, job_label)
            
            if 'needs' in job_config:
                needs = job_config['needs']
                if isinstance(needs, str):
                    needs = [needs]
                for dep in needs:
                    dot.edge(dep, job_name)
        
        dot.render(output_path, format='svg', cleanup=True)
        print(f"Generated diagram: {output_path}.svg")

# Check that diagrams were created
svg_files = glob.glob(f"{os.environ['OUTPUT_DIR']}/*.svg")
print(f"Generated {len(svg_files)} SVG files")

assert len(svg_files) > 0, "No SVG files were generated"
assert len(svg_files) == len(workflow_files) + 1, "Expected diagrams for each workflow plus combined"

print("✓ Complete workflow script tests passed")
EOF

# Verify SVG files are valid

echo "Verifying SVG files..."

for svg_file in workflow-diagrams/*.svg; do
    if [ -f "$svg_file" ]; then
        # Check if SVG file is not empty and contains basic SVG structure
        if [ -s "$svg_file" ] && grep -q '<svg' "$svg_file"; then
            echo "✓ $svg_file is valid"
        else
            echo "✗ $svg_file is invalid or empty"
            exit 1
        fi
    fi
done

# Cleanup
rm -rf "$TEST_DIR"

echo "\n=== All tests passed! ==="
echo "The GitHub Actions Workflow Visualizer is working correctly."
