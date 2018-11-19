#!/usr/bin/env bash

. /home/joakim/workout_secret
git pull --rebase
sudo pip3 install -r requirements.txt
systemctl restart worklog.service
