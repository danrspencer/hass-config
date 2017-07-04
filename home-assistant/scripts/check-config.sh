#!/usr/bin/env bash

set -e

echo -e "\033[1;34mChecking config... \033[0m"
sudo su -s /bin/bash homeassistant -c \
  "source /srv/homeassistant/bin/activate \
  && hass --script check_config"
