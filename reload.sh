#!/usr/bin/env bash

sudo git pull --rebase
sudo pip3 install -r requirements.txt
sudo systemctl restart worklog.service
