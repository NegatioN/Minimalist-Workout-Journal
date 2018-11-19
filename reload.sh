#!/usr/bin/env bash

git pull --rebase
sudo pip3 install -r requirements.txt
sudo systemctl restart worklog.service
