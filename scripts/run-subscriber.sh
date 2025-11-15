#!/bin/bash
# Run subscriber on Pico with mounted config
# Mounts PiPico directory so scripts can access .env from parent
#
# Usage: ./run-subscriber.sh [port]
# Author: Mae Capacite (C21348423)

PORT="${1:-rfc2217://localhost:4001}"

printf "Running subscriber with mounted config...\n"
printf "Port: %s\n\n" "$PORT"

cd ../PiPico
mpremote connect "$PORT" mount . run subscriber.py
