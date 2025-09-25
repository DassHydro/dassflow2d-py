#!/bin/bash

# Color codes for stdout
RST="\e[0m"
RED="\e[91m"
YLW="\e[33m" # Yellow
CYN="\e[36m" # Cyan

echo -e "${CYN}INFO: Creating virual environment directory${RST} ..."
python -m venv .venv
if [ $? -ne 0 ]; then # test exit code of previous command (to see if it failed)
    echo -e "${YLW}WARNING: Looks like you don't have the venv python module installed"
    echo -e "${CYN}INFO: Trying installation via pip${RST} ..."
    pip install virtualenv
    if [ $? -ne 0 ]; then
        echo -e "${ERR}ERROR: Installation failed, check how to install virtual environment module on your linux distribution${RST}"
        exit 1
    else
        echo -e "${CYN}INFO: Retrying to create virual environment directory${RST} ..."
        python -m venv .venv
        if [ $? -ne 0 ]; then
            echo -e "${ERR}ERROR: Cannot create virtual environment${RST}"
            exit 1
        fi
    fi
fi

# Install all requirements
source .venv/bin/activate
echo -e "${CYN}INFO: Installing Requirements${RST} ..."
pip install -r requirements.txt
