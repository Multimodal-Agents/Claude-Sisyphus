#!/usr/bin/env bash

HOOK_SRC="hooks/pre-push"
HOOK_DEST=".git/hooks/pre-push"

if [ "$1" = "on" ]; then
    if [ -f "$HOOK_DEST" ]; then
        echo "Push protection is already ON."
    else
        cp "$HOOK_SRC" "$HOOK_DEST"
        chmod +x "$HOOK_DEST"
        echo "Push protection is now ON. Git push is blocked."
    fi
elif [ "$1" = "off" ]; then
    if [ ! -f "$HOOK_DEST" ]; then
        echo "Push protection is already OFF."
    else
        rm "$HOOK_DEST"
        echo "Push protection is now OFF. Git push is allowed."
    fi
else
    echo "Usage: bash scripts/hook.sh [on|off]"
    echo ""
    if [ -f "$HOOK_DEST" ]; then
        echo "Current status: ON (pushes are blocked)"
    else
        echo "Current status: OFF (pushes are allowed)"
    fi
fi
