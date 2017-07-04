#!/usr/bin/env bash

set -e

echo
echo -e "\033[1;34mStopping Home Assistant... \033[0m"
sudo systemctl stop home-assistant@homeassistant.service

echo
echo -e "\033[1;34mUpgrading Home Assistant... \033[0m"
sudo su -s /bin/bash homeassistant -c \
  "source /srv/homeassistant/bin/activate \
  && pip3 install --upgrade homeassistant"

echo
echo -e "\033[1;34mStarting Home Assistant... \033[0m"
sudo systemctl start home-assistant@homeassistant.service
