#!/bin/bash
"""
Test runner for Nightly Docker Chaos Garden.

This script runs the unit tests in an isolated environment.
"""

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🧪 Running Nightly Docker Chaos Garden Tests${NC}"
echo "=" $(pwd)

# Check if we're in the right directory
if [ ! -f "src/chaos_garden.py" ]; then
    echo -e "${RED}❌ Error: chaos_garden.py not found. Make sure you're in the utility directory.${NC}"
    exit 1
fi

# Create a temporary Python environment for testing
echo -e "${YELLOW}📦 Setting up test environment...${NC}"
python3 -m venv /tmp/test_venv --clear
source /tmp/test_venv/bin/activate

# Install test dependencies
pip install docker pyyaml

# Add the src directory to Python path
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"

# Run the tests
echo -e "${YELLOW}🧪 Running unit tests...${NC}"
cd src
python -m pytest tests/test_chaos_garden.py -v

# Check if tests passed
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
else
    echo -e "${RED}❌ Some tests failed!${NC}"
    deactivate
    rm -rf /tmp/test_venv
    exit 1
fi

# Clean up
deactivate
rm -rf /tmp/test_venv

echo -e "${GREEN}🎉 Tests completed successfully!${NC}"
