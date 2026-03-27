# TODO

> **Latest session: March 26, 2026** - Mouse button shortcuts, Svorak Cmd+` fix, cross-Space window cycling.

---

## Active / Recent

### March 2026

21. **Mouse Button Shortcuts + Window Cycling** *(Mar 26, 2026)* ✅
    - [x] Created `mods/mouse_shortcuts.json` — unified single-rule file
    - [x] button4/5 → `<quote>`/`<before>` XML wraps in Ghostty/Zed
    - [x] button4 passes through as native mouse-back outside Ghostty/Zed
    - [x] button3 → Cross-Space window cycling via Hammerspoon
    - [x] Cmd+§ → Same-Space window cycling (rebound macOS symbolic hotkey 27)
    - [x] Opt+§ → Cross-Space window cycling via Hammerspoon
    - [x] Fixed Svorak Cmd+` (never worked before — no key produces backtick under Cmd-layer)
    - [x] Fixed ISO key code swap: Cmd+non_us_backslash → Cmd+grave_accent_and_tilde bridge
    - [x] Hammerspoon function with pre-loaded window.filter + explicit gotoSpace()
    - [x] Full path `/opt/homebrew/bin/hs` in shell_commands (launchd PATH issue)
    - [x] Single-rule pattern directive forged in CLAUDE.md
    - [x] Razer Viper 8KHz pointing device "Modify events" enabled
    - [x] Removed SuperWhisper global fallback on button4
    - [x] Docs updated, cheatsheets regenerated, committed and pushed
    - [ ] **MONITOR**: Cross-Space cycling may occasionally drag windows — gotoSpace timing edge case
    - [ ] **OPTIONAL**: Extend cheatsheet generator to include mouse shortcuts

### January 2026

20. **Ultrathink Removal & New Shortcuts** *(Jan 16, 2026)* ✅
    - [x] Removed "Ultrathink" suffix from ALL 33 keyboard shortcuts
    - [x] Removed "Ultrathink" suffix from ALL 25 Xbox controller mappings
    - [x] Caps+u: Changed from "Ultrathink" to "Unclear/examine assumptions"
    - [x] Caps+3: NEW - Resume from transcript (wraps clipboard in `<before>` tags)
    - [x] Caps+4: NEW - Paste with lines joined (clean prose)
    - [x] Xbox View (YES): Changed from "Ultrathink suffix" to "Proceed."
    - [x] DICT button: Increased delay from 2s to 3s
    - [x] Updated cheatsheet script (removed Ultrathink stripping, updated tiers)
    - [x] Regenerated both cheatsheets
    - [x] Updated CLAUDE.md, README.md, TODO.md

19. **Keyboard Shortcuts Composability Refactor** *(Jan 10, 2026)* ✅
    - [x] Refactored r/c/j/y for atomic composability
    - [x] Cheatsheet: Strip "Ultrathink" suffix from display
    - [x] Regenerated both cheatsheets

16. **Wired USB Xbox Controller Research** *(Jan 5-7, 2026)*
    - [x] Root cause: Xbox uses GIP protocol over USB, NOT HID (invisible to Karabiner)
    - [x] Built golden-narwhal12 driver at `~/Projects/xbox-controller-driver-macos/`
    - [ ] **TEST**: Run driver with wired controller (`sudo ./simulator`)

12. **Window Management & Couch Mode** *(Dec 2025)*
    - [x] LB+D-pad Left/Right for window switching
    - [ ] **BUG**: LB+D-pad window switching likely broken — Xbox config sends `grave_accent_and_tilde` directly, needs same ISO bridge fix as Cmd+§ keyboard binding (Svorak produces § not backtick)
    - [x] Hammerspoon cross-Space cycling implemented (Mar 2026)

---

## Backlog

- [ ] Extend cheatsheet generator to cover mouse shortcuts
- [ ] Clean up "Change grave accent (backtick) to..." rule still in Karabiner (disabled, historical)
- [ ] Test golden-narwhal12 wired Xbox driver
- [ ] D-pad Up/Down reliability investigation (known unreliable)

## Exploration

- [ ] Analog stick fine-tuning (deadzone, movement delay) — controller ergonomics
- [ ] Multiple Karabiner profiles (browsing vs coding vs testing)
- [ ] Screenshot automation (capture + attach to AI chat)
