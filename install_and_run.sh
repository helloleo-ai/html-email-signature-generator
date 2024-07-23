#!/bin/bash

# Update package list and upgrade existing packages
sudo apt-get update && sudo apt-get upgrade -y

# Install Python 3 and pip if not already installed
sudo apt-get install -y python3 python3-pip

# Install Python dependencies
pip3 install -r requirements.txt

# Launch the Flask application
python3 app.py