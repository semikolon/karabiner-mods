#!/bin/bash
# Delayed space for dictation - waits for SuperWhisper to finish, then types a space
LOG_FILE="/tmp/delayed_space.log"
echo "$(date): Script started" >> "$LOG_FILE"
sleep 1
echo "$(date): Sleep done, sending keystroke" >> "$LOG_FILE"
osascript -e 'tell application "System Events" to keystroke " "' 2>> "$LOG_FILE"
echo "$(date): Keystroke sent (exit code: $?)" >> "$LOG_FILE"
