#!/usr/bin/env bash

set -e

echo
echo -e "\033[1;34mInstalling App Daemon... \033[0m"

cd /opt
sudo git clone https://github.com/home-assistant/appdaemon.git
cd appdaemon
sudo pip3 install .
sudo mv conf/appdaemon.yaml.example conf/appdaemon.yaml
