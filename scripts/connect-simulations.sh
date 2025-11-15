#!/bin/bash
# Connect to both Wokwi simulated Picos using tmux
# Creates split-pane session with mpremote connections to RFC2217 ports
#
# Usage: ./connect-simulations.sh
# Author: Mae Capacite (C21348423)

set -e

SESSION_NAME="lab8-mqtt"

# Check dependencies
command -v tmux >/dev/null 2>&1 || { printf "tmux not found. Install: sudo dnf install tmux\n"; exit 1; }
command -v mpremote >/dev/null 2>&1 || { printf "mpremote not found. Install: pip install mpremote\n"; exit 1; }

# Attach to existing session if available
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    printf "Attaching to existing session...\n"
    tmux attach-session -t $SESSION_NAME
    exit 0
fi

printf "Creating tmux session: %s\n" "$SESSION_NAME"
printf "  Publisher:  rfc2217://localhost:4000\n"
printf "  Subscriber: rfc2217://localhost:4001\n\n"

# Create tmux session with vertical split
tmux new-session -d -s $SESSION_NAME -n "MQTT-Picos"
tmux split-window -h -t $SESSION_NAME

# Left pane: Publisher (port 4000)
tmux send-keys -t $SESSION_NAME:0.0 "printf '\033[1;32m=== Publisher (4000) ===\033[0m\n'" C-m
tmux send-keys -t $SESSION_NAME:0.0 "mpremote connect rfc2217://localhost:4000" C-m

# Right pane: Subscriber (port 4001)
tmux send-keys -t $SESSION_NAME:0.1 "printf '\033[1;34m=== Subscriber (4001) ===\033[0m\n'" C-m
tmux send-keys -t $SESSION_NAME:0.1 "mpremote connect rfc2217://localhost:4001" C-m

# Select publisher pane
tmux select-pane -t $SESSION_NAME:0.0

printf "Controls: Ctrl+b + arrows (switch) | Ctrl+b + d (detach) | Ctrl+d (exit)\n\n"

# Attach to session
tmux attach-session -t $SESSION_NAME
