#!/bin/bash
# Delayed space for dictation - waits for SuperWhisper to finish, then types a space
sleep 1
osascript -e 'tell application "System Events" to keystroke " "'
