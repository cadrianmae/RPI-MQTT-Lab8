#!/bin/bash
# Run publisher on Pico with mounted config
# Mounts PiPico directory so scripts can access .env from parent
#
# Usage: ./run-publisher.sh [port]
# Author: Mae Capacite (C21348423)

PORT="${1:-rfc2217://localhost:4000}"

printf "Running publisher with mounted config...\n"
printf "Port: %s\n\n" "$PORT"

cd ../PiPico
mpremote connect "$PORT" mount . run publisher.py
