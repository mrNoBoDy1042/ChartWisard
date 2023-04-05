#!/bin/bash

cd /opt/chartwizard/

#pull from the branch
git pull origin main

# Create venv
virtualenv venv -p python3
source ./venv/bin/activate

# followed by instructions specific to your project that you used to do manually
pip3 install -r requirements.txt
python3 -m uvicorn main:app 