#!/bin/bash
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
cd ics/
ln -fs caldav_repo/caldav caldav
