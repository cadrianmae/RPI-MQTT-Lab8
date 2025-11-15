#!/usr/bin/env bash

cd "$(dirname "$0")/.." || exit 1

printf "Formatting Python files with black...\n\n"

# Format PiPico files
black --line-length 88 PiPico/*.py

printf "\n✓ All Python files formatted!\n"
