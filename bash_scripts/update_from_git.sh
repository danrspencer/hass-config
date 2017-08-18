#!/usr/bin/env bash

date > /config/update_from_git.log
git reset --hard origin/master >> /config/update_from_git.log
git pull >> /config/update_from_git.log
