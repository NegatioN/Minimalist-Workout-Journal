#!/usr/bin/env bash

. /home/joakim/workout_secret
git pull --rebase
sudo pip3 install -r requirements.txt
sudo systemctl import-environment WORKOUT_SECRET
sudo systemctl restart worklog.service
