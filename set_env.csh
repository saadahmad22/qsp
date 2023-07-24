#!/usr/bin/env bash
# # !/bin/csh
python3 -m venv venv


# install flask module in project
pip3 install Flask

# add project dependencies
pip3 install flask-session
pip3 install passlib
pip3 install pytz
pip3 install datetime
pip3 install flask_wtf
pip3 install wtforms
pip3 install email_validator