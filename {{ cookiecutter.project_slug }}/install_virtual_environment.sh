#!/usr/bin/env bash

set -e

echo ">>> Installing virtual environment using venv."
python3 -m venv .venv
echo ">>> Installed! Now installing dependencies..."
.venv/bin/python -m pip install -q --upgrade pip
.venv/bin/python -m pip install -q -e .[dev]
echo -e ">>> Installed! Activating using \n>>> . .venv/bin/activate"