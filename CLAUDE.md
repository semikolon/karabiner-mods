# Karabiner Mods - Project Guide

## Overview

This project contains custom Karabiner-Elements keyboard modifications, primarily focused on text shortcuts that output common phrases for AI-assisted development with Claude Code.

## Key Files

- `mods/keyboard_text_shortcuts.json` - Main Karabiner config with all Caps+key shortcuts
- `mods/xbox_zed_claude.json` - Xbox controller mappings (25 actions: standalone + LB/RB combos + DICT)
- `scripts/generate_cheatsheet_ai.py` - AI-generated cheat sheets (Gemini 3 Pro Image)
- `docs/cheatsheet_keyboard.png` - Keyboard shortcuts visual reference
- `docs/cheatsheet_xbox.png` - Xbox controller mappings visual reference
- `docs/superwhisper_integration.md` - SuperWhisper vocabulary/replacements reference
- `docs/xbox_button_reference.md` - Xbox controller button mappings + technical details
- `docs/xbox_driver_macos_analysis.md` - Wired USB driver research (golden-narwhal12)
- `docs/antimicrox_analysis.md` - AntiMicroX architecture analysis
- `docs/eli5_shortcut_philosophy.md` - Design rationale for Caps+h clarity shortcut (Aristotle → Sellars → Quine → Žižek) ★
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

## CRITICAL RULE: Regenerate Cheat Sheets After Changes

**After ANY modification to keyboard or Xbox configs, you MUST regenerate the cheat sheets:**

```bash
.venv/bin/python scripts/generate_cheatsheet_ai.py
```

This ensures the visual documentation stays in sync with the actual shortcuts.

The script generates TWO separate images:
1. `docs/cheatsheet_keyboard.png` - Keyboard shortcuts (from `keyboard_text_shortcuts.json`)
2. `docs/cheatsheet_xbox.png` - Xbox controller (from `xbox_zed_claude.json`)

**Requires**: `GEMINI_API_KEY` environment variable

**Python Environment**: Uses project venv at `.venv/` with `google-genai` installed. If missing: `python3 -m venv .venv && .venv/bin/pip install google-genai`

## Adding New Shortcuts

1. Choose an unmapped Svorak key
2. Look up the QWERTY equivalent using the mapping above
3. Add the manipulator to `keyboard_text_shortcuts.json`
4. **Regenerate the cheat sheet** (see rule above)
5. Commit both the JSON and the updated `docs/cheatsheet_ai.png`

## Deploying New Mapping Files

**Standard procedure**: Use symlinks to Karabiner's complex_modifications folder.

```bash
ln -sf ~/Projects/karabiner-mods/mods/YOUR_FILE.json ~/.config/karabiner/assets/complex_modifications/
```

This allows:
- Version control of all mappings in this repo
- Clean separation between mapping clusters (keyboard, mouse, controller)

After creating the symlink, open Karabiner-Elements → Complex Modifications → Add rule → Enable the new rules.

**IMPORTANT: Reloading after edits** - Karabiner does NOT auto-reload complex modifications when the JSON file changes. You must manually: Remove the rule(s) → Re-add from the file. Otherwise old mappings remain active.

### Current Symlinks (December 2025)
```
~/.config/karabiner/assets/complex_modifications/
├── keyboard_text_shortcuts.json → mods/keyboard_text_shortcuts.json
└── xbox_zed_claude.json → mods/xbox_zed_claude.json
```

**Disabled** (removed from Karabiner):
- `app_specific_actions.json` - Old Cursor-specific mappings
- `mouse_browser_navigation.json` - Broken
- `mouse_safari_navigation.json` - Broken

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

## Prompt Engineering for Shortcuts

When designing shortcut phrases, follow these principles:

| Principle | Application | Example |
|-----------|-------------|---------|
| **Verb-first** | Start with action | "Document this" not "This should be documented" |
| **Single intent** | One action per shortcut | Composable, can combine multiple |
| **Positive framing** | Say what to do | "Find best file" not "Don't create new files" |
| **Scope constraint** | Bound the search/action | "30 recent .md files" limits scope |
| **Flexibility clause** | Allow judgment | "or several if necessary" |
| **Trailing space** | Enable composition | Allows chaining shortcuts |

**Intent separation**: Keep distinct operations atomic:
- **Enumerate** (r): List docs → "List 30 recent .md docs..."
- **Read** (c): Load context → "Read the most relevant 2-3 ones..."
- **Audit** (d): Check state → "Make sure docs are up to date with progress/reasoning..."
- **Output** (j): Write insights → "Document insights where appropriate..."
- **Challenge** (y): Examine assumptions → "Why are we going down this road?..."

## Current Shortcut Tiers

1. **Quick Responses** - Single words/short confirmations (p, s, g)
2. **Workflow Patterns** - Documentation, exploration, delegation (d, e, a, .)
3. **Combo Phrases** - Multi-step instructions (x, r, c, n)
   - r → Enumerate docs (list 30 recent .md files)
   - c → Read relevant docs (most relevant 2-3)
4. **Testing & Research** - Run tests, search online (t, ö, v)
5. **Semantic Actions** - Examine, wait, summarize, fix, clarity, document, challenge, zoom (u, w, å, f, h, j, y, ä)
   - u → Unclear/examine assumptions (rank weakest to strongest)
   - h → Clarity / load-bearing idea (analogy + perspectives + what's left out) ★ favorite
   - j → Document insights where appropriate
   - y → Challenge assumptions (deeper why)
   - ä → Zoom out (open loops check)
6. **Slash Commands** - Claude Code slash commands (m, k, i, b, l, o, q, z)
   - m → /recall (memory)
   - k → /capture (keep)
   - i → /significance (important)
   - b → /debug-session (bug)
   - l → /ui-prototype (layout)
   - o → /consensus-consult (opinions)
   - q → /docs-review (quality)
   - z → /total-recap
7. **Utility** - Clipboard/selection helpers (2, 3, 4)
   - 2 → Quote selection (copies, wraps in `<quote>` tags)
   - 3 → Resume from selection (copies, wraps in `<before>` tags)
   - 4 → Paste with lines joined (clean prose)

## Xbox Controller Integration

See `docs/xbox_button_reference.md` for full documentation including visual layout and session learnings.

### Current Mappings (January 2026)

| Label | Button | Code | Action |
|-------|--------|------|--------|
| **YES** | View | button11 | "Proceed." |
| **DICT** | Menu | button12 | SuperWhisper toggle + delayed suffix space (3s) |
| **NO** | Guide | button13 | Escape |
| **SPECS** | B | button2 | "Sit rep." |
| **STANDUP** | A | button1 | "What's next according to the plan?" |
| *(none)* | X | button4 | "Read up on the relevant docs..." |
| *(none)* | Y | button5 | "Make sure key docs are up to date..." |
| *(none)* | LB | button7 | "Don't make changes. Explore..." |
| *(none)* | RB | button8 | "Put a subagent on researching..." |
| *(none)* | D-pad Left | generic_desktop | Delete Word (Opt+Backspace) |
| *(none)* | D-pad Right | generic_desktop | Enter key |
| *(none)* | L-Stick | button14 | /total-recap (session recovery) |
| *(none)* | R-Stick | button15 | "Commit everything in (chrono)logical groups. Then push." |

### Xbox Controller Files
- `mods/xbox_zed_claude.json` - All controller mappings (25 unique actions: 13 standalone + 12 combos)
- `docs/xbox_button_reference.md` - Definitive button reference with technical details
- `docs/xbox_driver_macos_analysis.md` - Wired USB driver research (golden-narwhal12)
- `docs/antimicrox_analysis.md` - AntiMicroX architecture study (Linux/Windows only)

**Note**: D-pad uses `generic_desktop: dpad_left` syntax, not `pointing_button`.

### Wired USB Support (January 2026)

**Key finding**: Xbox controller uses different protocols depending on connection:
- **Bluetooth**: Standard HID → Karabiner works ✅
- **Wired USB**: GIP protocol → Karabiner cannot see buttons ❌

Karabiner config includes both Product IDs (2834 wired, 2835 Bluetooth) but wired requires the golden-narwhal12 userspace driver for button input.

**Driver location**: `~/Projects/xbox-controller-driver-macos/` (built, ready to test)

## SuperWhisper Integration

See `docs/superwhisper_integration.md` for complete reference including:
- Vocabulary vs Replacements (when to use each)
- File locations (`~/Documents/superwhisper/settings/settings.json`)
- ISO keyboard considerations (`non_us_backslash` for Swedish)
- Recommended vocabulary aligned with keyboard/controller shortcuts
- Slash command trigger replacements
