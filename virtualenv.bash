#!/bin/bash

# Convert the passed parameter to lowercase
paramVal=$(echo "$1" | tr '[:upper:]' '[:lower:]')
echo "Passed Parameter: $paramVal"

# Get the current project directory folder path
CWD=$(pwd)


# Determine whether to create and activate a virtual environment 'venv' based on the passed parameter
if [[ "$paramVal" == "set" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv

    echo "Activating virtual environment now..."
    if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
        echo "Script should be called without being sourced"
        echo "Venv generation usage: source $CWD/$(basename "$(test -L "$0" && readlink "$0" || echo "$0")") set"
    else
        source "$CWD/venv/bin/activate"
        echo "Virtual environment activated!"
    fi        
elif [[ "$paramVal" == "activate" ]]; then    
    echo "Activating virtual environment now..."
    if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
        echo "Script should be called without being sourced"
        echo "Venv usage: source $CWD/$(basename "$(test -L "$0" && readlink "$0" || echo "$0")") activate"
    else
        source "$CWD/venv/bin/activate"
        echo "Virtual environment activated!"
    fi        
elif [[ "$paramVal" == "deactivate" ]]; then   
    # Check if VIRTUAL_ENV variable is empty
    [[ -z "$VIRTUAL_ENV" ]]
    INVENV=$?

    # Check if VIRTUAL_ENV is empty (no active virtual environment)
    if [[ $INVENV -eq 0 ]]; then
        echo "No active virtual environment found!"
        echo "Usage: source $CWD/$(basename "$(test -L "$0" && readlink "$0" || echo "$0")") <set|activate|deactivate>"
    else
        echo "Deactivating virtual environment..."
        deactivate
        echo "Virtual environment deactivated!"
    fi
else
    echo "Usage: source $CWD/$(basename "$(test -L "$0" && readlink "$0" || echo "$0")") <set|activate|deactivate>"
fi
