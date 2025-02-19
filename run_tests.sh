#!/bin/bash

# Set the PYTHONPATH to the root of the project
export PYTHONPATH=$(pwd)

# Create the log directory if it does not exist
mkdir -p log

# Run the system test
python3 tests/systemtest.py