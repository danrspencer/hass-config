#!/usr/bin/env bash

echo '{ "command": "clearall"}' | nc 192.168.0.27 19444
echo "{\"effect\": {\"name\": \"$1\"}, \"command\": \"effect\", \"priority\": 100 }" | nc 192.168.0.27 19444
