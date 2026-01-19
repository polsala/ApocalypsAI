#!/bin/bash

# Ensure the tests directory and its contents are present
if [ ! -d "tests" ] || [ ! -f "tests/test_main.py" ]; then
    echo "Error: Test files not found. Please ensure 'tests/test_main.py' exists."
    exit 1
fi

# Ensure the src directory and its contents are present
if [ ! -d "src" ] || [ ! -f "src/main.py" ]; then
    echo "Error: Source files not found. Please ensure 'src/main.py' exists."
    exit 1
fi

# Ensure requirements.txt is present
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found."
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install Python dependencies."
        exit 1
    fi
fi

# Run the tests
echo "Running Python tests..."
python -m unittest discover -s tests -p "test_*.py"

if [ $? -eq 0 ]; then
    echo "All tests passed successfully!"
    exit 0
else
    echo "Some tests failed."
    exit 1
fi
