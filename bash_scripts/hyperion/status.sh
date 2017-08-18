#!/usr/bin/env bash

echo '{"command": "serverinfo"}' | nc -i 1 192.168.0.27 19444 | grep -vq '{"priority":0}'
