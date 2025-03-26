#!/bin/bash
set -e

# Verify we are in the correct directory
if [ "$(basename "$PWD")" != "glm" ]; then
    echo "Error: Script must be run from within the 'glm' directory."
    exit 1
fi

echo "Updating package list..."
sudo apt-get update

echo "Installing software..."
sudo apt-get install -y git
sudo apt-get install -y vim # Text editor of choice
sudo apt-get install -y python3-pip

echo "Creating Python virtual environment..."
python3 -m venv venv
. venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping pip install."
fi

echo "Setup complete!"