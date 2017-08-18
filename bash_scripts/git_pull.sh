#!/usr/bin/env bash

echo "Resetting to origin/master..."
git reset --hard origin/master

echo "Pulling..."
git pull
