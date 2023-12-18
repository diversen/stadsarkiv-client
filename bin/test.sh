#!/bin/sh

# This script runs tests
./venv/bin/python -m unittest tests/config-default/*.py

# Test teater client
export CONFIG_DIR="example-config-teater"
./venv/bin/python -m unittest tests/config-teater/*.py

# Test aarhus
export CONFIG_DIR="example-config-aarhus"
./venv/bin/python -m unittest tests/config-aarhus/*.py