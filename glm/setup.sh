#!/bin/bash
set -e

echo "Updating package list..."
sudo apt-get update

echo "Installing software..."
sudo apt-get install -y vim      # Text editor of choice
sudo apt-get install -y minicom  # Test serial communication
sudo apt-get install -y python3-pip

cd ~/glm || { echo "Directory ~/glm not found. Exiting."; exit 1; }

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