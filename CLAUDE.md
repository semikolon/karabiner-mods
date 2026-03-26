# Karabiner Mods - Project Guide

## Overview

This project contains custom Karabiner-Elements keyboard modifications, primarily focused on text shortcuts that output common phrases for AI-assisted development with Claude Code.

## Key Files

- `mods/keyboard_text_shortcuts.json` - Main Karabiner config with all Caps+key shortcuts
- `mods/mouse_shortcuts.json` - Mouse button mappings (button3/4/5 with app-specific and global rules)
- `mods/xbox_zed_claude.json` - Xbox controller mappings (25 actions: standalone + LB/RB combos + DICT)
- `scripts/generate_cheatsheet_ai.py` - AI-generated cheat sheets (Gemini 3 Pro Image)
- `docs/cheatsheet_keyboard.png` - Keyboard shortcuts visual reference
- `docs/cheatsheet_xbox.png` - Xbox controller mappings visual reference
- `docs/superwhisper_integration.md` - SuperWhisper vocabulary/replacements reference
- `docs/xbox_button_reference.md` - Xbox controller button mappings + technical details
- `docs/xbox_driver_macos_analysis.md` - Wired USB driver research (golden-narwhal12)
- `docs/antimicrox_analysis.md` - AntiMicroX architecture analysis
- `docs/eli5_shortcut_philosophy.md` - Design rationale for Caps+h clarity shortcut (Aristotle → Sellars → Quine → Žižek) ★
- `docs/shortcut_ideas.md` - Research and ideas for future shortcuts (XML wrapper family, workflow enhancers)
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

### Unmapped Keys (January 2026)

All 30 letter keys are mapped. Number row status:

| Key | Status | Ergonomics | Notes |
|-----|--------|------------|-------|
| **1** | Available | ★☆☆☆☆ | Left pinky area - awkward |
| **2** | Mapped | - | Quote selection (`<quote>` tags) |
| **3** | Mapped | - | Resume from selection (`<before>` tags) |
| **4** | Mapped | - | Paste with lines joined |
| **5** | Mapped | - | ELI5 / load-bearing idea |
| **6** | Available | ★★★★★ | Right index - best available |
| **7** | Available | ★★★★☆ | Right index/middle |
| **8** | Available | ★★★★☆ | Right middle |
| **9** | Available | ★★★☆☆ | Right ring |
| **0** | Available | ★★★☆☆ | Right pinky |

*Ergonomics based on left pinky holding Caps Lock. Right-hand keys (6-0) avoid stretch conflicts.*

**See**: `docs/shortcut_ideas.md` for future ideas (XML wrapper family: `<context>`, `<code>`, `<error>`, `<output>`).

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

## Rule Structure: One Rule Per File (MANDATORY)

All manipulators in a Karabiner JSON file MUST be grouped into a **single rule** so they appear as one entry in the Complex Modifications UI. This allows deleting and re-adding all mappings in one click when reloading after edits. Use per-manipulator `description` fields for individual labels.

**Pattern** (see `xbox_zed_claude.json` and `mouse_shortcuts.json`):
```json
{ "title": "...", "rules": [{ "description": "Group label", "manipulators": [...all mappings...] }] }
```

**Anti-pattern**: Multiple rules in `rules[]` → each shows as a separate row → tedious to reload.

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

### Current Symlinks (March 2026)
```
~/.config/karabiner/assets/complex_modifications/
├── keyboard_text_shortcuts.json → mods/keyboard_text_shortcuts.json
├── mouse_shortcuts.json → mods/mouse_shortcuts.json
└── xbox_zed_claude.json → mods/xbox_zed_claude.json
```

**Disabled** (removed from Karabiner):
- `app_specific_actions.json` - Old Cursor-specific mappings
- `mouse_browser_navigation.json` - Broken
- `mouse_safari_navigation.json` - Broken
- `mouse_superwhisper.json` - Superseded by `mouse_shortcuts.json`

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
- **Audit** (d): Check state → "Make sure docs are up to date with findings/progress/reasoning/decisions/ideas..."
- **Output** (j): Write insights → "Document insights where appropriate..."
- **Challenge** (y): Examine assumptions → "Why are we going down this road?..."

## Current Shortcut Categories

1. **Quick & Utility** - Short confirmations + clipboard helpers (p, s, g, 2, 3, 4)
   - p → Proceed | s → Sit rep | g → Git state
   - 2 → Quote selection (`<quote>` tags) | 3 → Resume (`<before>` tags) | 4 → Paste joined
2. **Workflow & Research** - Docs, delegation, testing (d, e, a, ., x, r, c, n, t, ö, v)
   - r → Enumerate docs | c → Read relevant 2-3 | d → Doc audit
   - a → Subagent delegation | e → Explore | t → Run tests | v → Research online
3. **Thinking** - Deep reflection shortcuts (u, w, å, f, h, j, y, ä)
   - u → Examine assumptions (rank weakest→strongest)
   - w → Wait/hold before decisions
   - h → Clarity / load-bearing idea ★ favorite
   - y → Challenge assumptions (deeper why)
   - ä → Zoom out (open loops)
4. **Slash Commands** - Claude Code commands (m, k, i, b, l, o, q, z)
   - m → /recall | k → /capture | i → /significance | b → /debug-session
   - l → /ui-prototype | o → /consensus-consult | q → /docs-review | z → /total-recap

## Mouse Button Shortcuts (March 2026)

**Device**: Razer Viper 8KHz (USB). Must have "Modify events" enabled on the **pointing device** entry in Karabiner → Devices (the mouse appears twice — keyboard + pointing device).

| Button | In Ghostty/Zed | Elsewhere |
|--------|----------------|-----------|
| **button3** (scroll click) | Cross-Space window cycling | Cross-Space window cycling |
| **button4** (back/thumb) | `<quote>` wrap (= Caps+2) | Native (browser back, etc.) |
| **button5** (forward/thumb) | `<before>` wrap (= Caps+3) | Native (browser forward, etc.) |

### § Key Family (all on one physical key, differentiated by modifier)

| Modifier | Action | Mechanism | Latency |
|----------|--------|-----------|---------|
| § alone | SuperWhisper toggle | Native app hotkey | instant |
| Ctrl+§ | Voice assistant (Ruby) | Native app hotkey | instant |
| Cmd+§ | Same-Space window cycling | Karabiner key_code remap → macOS system shortcut | instant |
| Opt+§ | Cross-Space window cycling | Karabiner → Hammerspoon `hs.window.filter` | ~100ms |

### Svorak + Cmd+` Window Cycling (deep investigation)

- macOS system shortcuts match on **character produced under the Cmd-layer**, not raw key code
- On Svorak, key code 24 (`equal_sign`) produces backtick normally, but `-` (hyphen) when Cmd is held — **no key on Svorak produces backtick with Cmd held**. This is why Cmd+` never worked.
- **Fix**: Rebound macOS symbolic hotkey 27 from `(96, 24, 1048576)` to `(167, 50, 1048576)` — expects § (char 167) + key code 50 + Cmd. Applied via `defaults write com.apple.symbolichotkeys` + `activateSettings -u`
- **ISO key code swap** (Karabiner v15 bug #3984): Physical § sends `non_us_backslash` (key code 10), virtual keyboard sends key code 50 for `grave_accent_and_tilde`. Bridged with a Karabiner rule: Cmd+`non_us_backslash` → Cmd+`grave_accent_and_tilde`

### Cross-Space Cycling (Hammerspoon)

**Dependency**: Function `cycleAppWindowsAcrossSpaces()` in `~/.hammerspoon/init.lua` (chezmoi-managed from `dotfiles/home/dot_hammerspoon/init.lua`). Uses `hs.window.filter` (only API that sees windows across all Spaces) + `hs.spaces.gotoSpace()` to explicitly switch Space before focusing, preventing macOS from dragging windows to the current Space.

**Shell command gotcha**: Karabiner `shell_command` runs via launchd with minimal PATH. Must use full path `/opt/homebrew/bin/hs`, not bare `hs`. Pre-load `hs.window.filter` at startup (`require("hs.window.filter")`) to avoid 5+ second lazy-load penalty on first call.

### Other Notes

**Ghostty middle-click paste**: Hardcoded (Unix/X11 convention), cannot be disabled. Overridden by Karabiner intercepting button3 before Ghostty receives it.

**App bundle IDs**: Ghostty = `com.mitchellh.ghostty`, Zed = `dev.zed.Zed`

**Razer Viper 8KHz**: Ambidextrous — side buttons on both sides send identical button4/button5. DPI button on underside (not useful mid-flow). Registers as keyboard + pointing device over USB; must enable "Modify events" on the pointing device entry only.

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
| *(none)* | Y | button5 | Doc audit (matches Caps+d) |
| *(none)* | LB | button7 | Wait/hold (matches Caps+w) |
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
