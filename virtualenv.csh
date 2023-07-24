#!/bin/bash
# NOTE: this script use source command to call another script, it is required to execute this script file with source command
# here is test run command
# source virtualenv.csh set  => Creates and sets vnev
# source virtualenv.csh => destroys venev

#convert passed parameter to lower case string
paramVal=$(echo "$1" | tr '[:upper:]' '[:lower:]') 
echo "Passed Parameter $paramVal"

# Takes an argument and determine create and activate virtual environment 'venv' based on passed parameter as 'set'
if [[ ($paramVal == "set") ]];  then
	echo "Creating venev..."
	python3 -m venv venv

	# get current project directory folder path as source command need full path to shell file to run it
	CWD=$(pwd)

	echo "Activating venev now..."
	# call / source activate shell with the full path
	source "$CWD/venv/bin/activate"
	
	echo "vnev activated!"
else
	# Copies virtual environment path to VIRTUAL_ENV variable
	[[ "$VIRTUAL_ENV" == "" ]]; INVENV=$?

	# Check VIRTUAL_ENV variable empty, in that case no active virtual environment available
	if [[ -z "$VIRTUAL_ENV" ]]; then
		echo "No active vnev environment found!"
	else
        echo "Deactivating venv environment ..."
        # deactivate environment
        deactivate
        echo "vnev deactivated!"
	fi
fi
