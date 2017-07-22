#!/usr/bin/env bash

echo "{\"effect\": {\"name\": \"Green mood blobs\"}, \"command\": \"effect\", \"priority\": 100 }" | nc 192.168.0.27 19444
