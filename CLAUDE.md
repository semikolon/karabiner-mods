# Karabiner Mods - Project Guide

## Overview

This project contains custom Karabiner-Elements keyboard modifications, primarily focused on text shortcuts that output common phrases for AI-assisted development (Claude Code with "Ultrathink" trigger).

## Key Files

- `mods/keyboard_text_shortcuts.json` - Main Karabiner config with all shortcuts
- `scripts/generate_cheatsheet.py` - Generates visual cheat sheet from config
- `docs/cheatsheet.svg` - Visual reference of all shortcuts
- `.claude/commands/analyze-shortcuts.md` - Slash command for analyzing message history

## Keyboard Layout

Uses **Svorak** keyboard layout. All shortcuts are defined by their Svorak key but the JSON config uses QWERTY `key_code` values (what the physical key sends).

### Svorak → QWERTY Mapping Reference
```
Svorak: å ä ö p y f g c r l
QWERTY: q w e r t y u i o p

Svorak: a o e u i d h t n s
QWERTY: a s d f g h j k l ;

Svorak: . q j k x b m w v z
QWERTY: z x c v b n m , . /
```

## CRITICAL RULE: Regenerate Cheat Sheet After Changes

**After ANY modification to `mods/keyboard_text_shortcuts.json`, you MUST regenerate the cheat sheet:**

```bash
python3 scripts/generate_cheatsheet.py
```

This ensures the visual documentation stays in sync with the actual shortcuts.

The script:
1. Reads all shortcuts from the JSON config
2. Extracts key mappings and output text
3. Groups by tier (Quick/Workflow/Combo/Testing/Semantic)
4. Generates `docs/cheatsheet.svg`

## Adding New Shortcuts

1. Choose an unmapped Svorak key
2. Look up the QWERTY equivalent using the mapping above
3. Add the manipulator to `keyboard_text_shortcuts.json`
4. **Regenerate the cheat sheet** (see rule above)
5. Commit both the JSON and the updated cheatsheet.svg

### Shell Command Pattern

All shortcuts use clipboard+paste with restoration:
```json
{
  "shell_command": "osascript -e 'set prev to the clipboard' -e 'set the clipboard to \"YOUR TEXT \"' -e 'tell application \"System Events\" to keystroke \"v\" using command down' -e 'delay 0.1' -e 'set the clipboard to prev'"
}
```

**Important**: All outputs should end with a trailing space for composability.

For text with apostrophes, use double-quote escaping:
```json
{
  "shell_command": "osascript -e 'set prev to the clipboard' -e \"set the clipboard to \\\"What's next? \\\"\" -e 'tell application \"System Events\" to keystroke \"v\" using command down' -e 'delay 0.1' -e 'set the clipboard to prev'"
}
```

## Shortcut Analysis

Use `/analyze-shortcuts` to analyze historical Claude Code messages and suggest new shortcuts based on:
- Frequently typed phrases
- Semantic clusters (same intent, different words)
- Combo patterns (multi-step instructions)

## Current Shortcut Tiers

1. **Quick Responses** - Single words/short confirmations (u, c, y, p, s, g)
2. **Workflow Patterns** - Documentation, exploration, delegation (d, e, a)
3. **Combo Phrases** - Multi-step instructions (x, r, n)
4. **Testing & Research** - Run tests, search online (t, ö)
5. **Semantic Actions** - Wait, summarize, fix, explain (w, å, f, h)
