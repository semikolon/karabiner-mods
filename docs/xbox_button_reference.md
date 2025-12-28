# Xbox Controller Button Reference

> **Purpose**: Definitive mapping between physical controller buttons, their labels, and Karabiner codes.
>
> **Controller**: Xbox Wireless Controller (Vendor ID: 1118, Product ID: 2835)
> **Last Updated**: December 28, 2025

## Complete Button Mapping

| Physical Label | Physical Button | Icon/Description | Karabiner Code | Standalone Action | LB+ Combo | RB+ Combo |
|----------------|-----------------|------------------|----------------|-------------------|-----------|-----------|
| **YES** | View Button | Two overlapping rectangles | `button11` | " Ultrathink " (suffix) | - | - |
| **DICT** | Menu Button | Three horizontal lines | `button12` | SuperWhisper | - | - |
| **NO** | Guide Button | Glowing Xbox logo | `button13` | Escape | - | - |
| **SPECS** | B Button | Red "B" on face | `button2` | "Sit rep. Ultrathink " | Research extensively | Key "2" (CC) |
| **STANDUP** | A Button | Green "A" on face | `button1` | "What's next...?" | Zoom out/open loops | Key "1" (CC) |
| *(unlabeled)* | X Button | Blue "X" on face | `button4` | Context refresh | Fix this | Key "3" (CC) |
| *(unlabeled)* | Y Button | Yellow "Y" on face | `button5` | Doc coherence check | Summarize briefly | Pull and push |
| *(modifier)* | LB | Left Bumper | `button7` | "Explore..." (tap) | **MODIFIER** | - |
| *(modifier)* | RB | Right Bumper | `button8` | "Subagent..." (tap) | - | **MODIFIER** |
| *(unlabeled)* | D-pad Left | Left arrow on D-pad | `generic_desktop: dpad_left` | Delete Word | Prev window | - |
| *(unlabeled)* | D-pad Right | Right arrow on D-pad | `generic_desktop: dpad_right` | Enter key | Next window | - |
| *(unlabeled)* | Left Stick Click | Press joystick | `button14` | /total-recap | - | - |
| *(unlabeled)* | Right Stick Click | Press joystick | `button15` | Commit+Push | - | - |

## Visual Layout

```
                    [LB button7]              [RB button8]
                    MODIFIER + tap="Explore"  MODIFIER + tap="Subagent"
                         ___________________________
                        /  SPECS→[B]    [Y]←DocCheck\
     DICT→[☰ button12] |       STANDUP→[A]  [X]←Refresh|
          [ⓧ button13]←NO                             |
    YES→[⧉ button11]   |                              |
                       |   [Left Stick]  [Right Stick]|
   /total-recap→(click)|      ↑              ↑←Git    |
                       |DelWord←[D-pad]→Enter         |
                        \     ↓ (avoid)              /
                         ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

LB+ Combos: A=ZoomOut B=Research X=Fix Y=Summarize D←=PrevWin D→=NextWin
RB+ Combos: A=Key1 B=Key2 X=Key3 Y=PullPush
```

## Button Categories

### Labeled Buttons (physical labels on controller)
| Label | Button | Action | Notes |
|-------|--------|--------|-------|
| YES | button11 | " Ultrathink " (suffix) | Append to any message/dictation |
| DICT | button12 | SuperWhisper | Via `non_us_backslash` (ISO keyboards) |
| NO | button13 | Escape | Cancel/interrupt (requires firm press) |
| SPECS | button2 | "Sit rep. Ultrathink " | Status report request |
| STANDUP | button1 | "What's next according to the plan? Ultrathink " | Progress check |

### Unlabeled Buttons (workflow actions)
| Button | Action | Category |
|--------|--------|----------|
| X (button4) | Context refresh | Preparation |
| Y (button5) | Doc coherence check | Documentation |
| LB (button7) | Explore without changes | Research |
| RB (button8) | Delegate to subagent | Delegation |
| D-pad Left | Delete Word (Opt+Backspace) | Recovery |
| D-pad Right | Enter key | Confirmation |
| L-Stick (button14) | /total-recap | Session recovery |
| R-Stick (button15) | Git workflow finisher | Git |

## Reliability Notes

### Reliable Buttons (recommended for critical workflows)
- `button1` (A) - STANDUP
- `button2` (B) - SPECS
- `button4` (X)
- `button5` (Y)
- `button7` (LB)
- `button8` (RB)
- `button11` (View) - YES
- `button12` (Menu) - DICT
- `button13` (Guide) - NO (requires firmer press)
- `button14` (Left Stick Click)
- `button15` (Right Stick Click)
- **D-pad Left/Right** - Reliable when pressed individually (use `generic_desktop` syntax)

### Unreliable/Unmappable (avoid for critical workflows)
- **D-pad Up/Down**: Unreliable. "Up" often registers as "Right", simultaneous presses cause confusion.
- **LT/RT Triggers**: Not detectable by Karabiner-EventViewer.
- **Share Button**: Captured by macOS `gamecontrollerd` before reaching Karabiner - completely invisible to EventViewer.

## D-pad Technical Details

### What Works
- **Left and Right are reliable on their own** (tested December 2025)
- Use `generic_desktop` syntax instead of `pointing_button`:
  ```json
  "from": {
      "generic_desktop": "dpad_left"
  }
  ```

### What Doesn't Work
- **Up frequently registers as Right**
- **Down alone seems okay, but combined with Left/Right gets confused**
- Multiple directions firing simultaneously when pressing diagonally

### Recommendation
Only use D-pad Left and D-pad Right for non-critical, recoverable actions.

### Why Opt+Backspace instead of Cmd+Z?
**Cmd+Z doesn't work in terminals** (Ghostty, Terminal.app, etc.) - terminals use different undo semantics. Option+Backspace (delete word) works universally across:
- Terminal emulators (Ghostty, where Claude Code often runs)
- GUI editors (Zed, VS Code)
- Text fields in browsers
- Any macOS text input

## Share Button Limitation

The Xbox Share button is **completely invisible to Karabiner-Elements**.

### Root Cause
macOS captures the Share button at the system level via `gamecontrollerd` before it reaches user-space applications. This is a macOS limitation, not a Karabiner bug.

### Workarounds (not tested)
1. **Wired USB-C connection**: May bypass Bluetooth HID handling
2. **Third-party tools**: Enjoyable, Joystick Doctor, or Contanki (Anki controller plugin)
3. **Xbox Accessories app**: May allow remapping at firmware level

### Current Status
Share button remains unmapped. D-pad Left provides Delete Word as a quick recovery action.

## File Configuration

### Active Configuration Files
| File | Purpose | Status |
|------|---------|--------|
| `mods/xbox_zed_claude.json` | Main controller mappings (13 inputs) | **ACTIVE** |
| `mods/dictation_toggle.json` | DICT button (button12) only | **ACTIVE** |
| `mods/keyboard_text_shortcuts.json` | Caps+key text shortcuts | **ACTIVE** |

### Deprecated/Disabled Files
| File | Purpose | Status |
|------|---------|--------|
| `mods/app_specific_actions.json` | Old Cursor-specific mappings | **DISABLED** |
| `mods/mouse_browser_navigation.json` | Mouse button browser nav (broken) | **DISABLED** |
| `mods/mouse_safari_navigation.json` | Mouse button Safari nav (broken) | **DISABLED** |

**Note**: `dictation_toggle.json` and `xbox_zed_claude.json` don't conflict - dictation_toggle handles button12 exclusively, while xbox_zed_claude handles all other buttons plus D-pad.

## Karabiner JSON Pattern

### Text Output (clipboard+paste with restoration)
```json
{
    "type": "basic",
    "from": {
        "pointing_button": "button1"
    },
    "to": [
        {
            "shell_command": "osascript -e 'set prev to the clipboard' -e 'set the clipboard to \"Your text here \"' -e 'tell application \"System Events\" to keystroke \"v\" using command down' -e 'delay 0.1' -e 'set the clipboard to prev'"
        }
    ],
    "conditions": [
        {
            "type": "device_if",
            "identifiers": [
                {
                    "vendor_id": 1118,
                    "product_id": 2835
                }
            ]
        }
    ]
}
```

### Text with Apostrophes (escape handling)
```json
{
    "shell_command": "osascript -e 'set prev to the clipboard' -e \"set the clipboard to \\\"What's next? \\\"\" -e 'tell application \"System Events\" to keystroke \"v\" using command down' -e 'delay 0.1' -e 'set the clipboard to prev'"
}
```

### Key Press (simple key code)
```json
{
    "to": [
        {
            "key_code": "return_or_enter"
        }
    ]
}
```

### D-pad Input (uses generic_desktop, not pointing_button)
```json
{
    "type": "basic",
    "from": {
        "generic_desktop": "dpad_left"
    },
    "to": [
        {
            "key_code": "delete_or_backspace",
            "modifiers": ["option"]
        }
    ],
    "conditions": [
        {
            "type": "device_if",
            "identifiers": [
                {
                    "vendor_id": 1118,
                    "product_id": 2835
                }
            ]
        }
    ]
}
```

**Important**: D-pad uses `generic_desktop` key, not `pointing_button`. Valid values: `dpad_left`, `dpad_right`, `dpad_up`, `dpad_down`.

## Session Learnings (December 21, 2025)

### SuperWhisper Integration
- **Issue**: button12 was detected in EventViewer but SuperWhisper didn't activate
- **Root Cause 1**: `dictation_toggle.json` was sending `Ctrl+Ctrl` (macOS dictation)
- **Root Cause 2**: Then tried `grave_accent_and_tilde`, but on ISO keyboards (Swedish), that's the wrong key!
- **Solution**: SuperWhisper uses `carbonKeyCode: 50` which maps to `non_us_backslash` on ISO keyboards (the § key above Tab)
- **Fix**: Updated `dictation_toggle.json` to send `non_us_backslash`
- **Config location**: `~/Library/Preferences/com.superduper.superwhisper.plist`

### ISO vs ANSI Keyboard Key Codes
- On **ANSI** keyboards: key above Tab = `grave_accent_and_tilde` (backtick)
- On **ISO** keyboards (Swedish): key above Tab = `non_us_backslash` (§ section sign)
- SuperWhisper stores hotkeys as Carbon key codes (legacy Apple format)
- Carbon key code 50 = the physical key above Tab, regardless of layout

### Global vs App-Specific Mappings
- **Previous**: Mappings had `frontmost_application_if` conditions limiting them to Zed
- **Current**: All mappings are global (only `device_if` condition) - work in any application
- **Rationale**: Claude Code text shortcuts are useful across all apps (terminals, browsers, etc.)

### Button Detection Tips
- Use **Karabiner-EventViewer** to verify button codes
- Guide button (button13) requires a firm press - light taps may not register
- If a button shows in EventViewer but action doesn't fire, check for conflicting rules in other JSON files

## Session Learnings (December 22, 2025)

### D-pad Left/Right Are Usable
- **Discovery**: Despite earlier notes about D-pad unreliability, Left and Right work reliably when pressed individually
- **Syntax**: Must use `generic_desktop: dpad_left` (NOT `pointing_button`)
- **Limitation**: Up/Down remain unreliable (Up often registers as Right)
- **Best practice**: Only bind D-pad Left/Right to recoverable, non-critical actions

### Terminal Compatibility
- **Issue**: Cmd+Z (Undo) doesn't work in terminals (Ghostty, Terminal.app)
- **Solution**: Use Opt+Backspace (Delete Word) instead - works universally
- **Context**: Primary Claude Code usage is in Ghostty terminal, not GUI editors

### Configuration Cleanup
- Removed deprecated `app_specific_actions.json` (old Cursor-specific mappings)
- Removed broken `mouse_browser_navigation.json` and `mouse_safari_navigation.json`
- Active configs now: `xbox_zed_claude.json`, `dictation_toggle.json`, `keyboard_text_shortcuts.json`

## Button Modifier Combos (IMPLEMENTED - December 2025)

### Architecture

**LB/RB now function as modifiers** using `set_variable`/`variable_if` pattern:
- **Tap alone**: Fires original action
- **Hold + other button**: Fires combo action

### LB+ Layer (Exploration/Comprehension)

| Combo | Action | Phrase/Key |
|-------|--------|------------|
| LB tap | Explore | "Don't make changes. Explore and report back. Ultrathink " |
| LB+A | Zoom out | "Let's zoom out. How did we get here? What were we in the middle of? Are there any open loops we forgot about? Ultrathink " |
| LB+B | Research | "Research this extensively online. Ultrathink " |
| LB+X | Fix | "Fix this. Ultrathink " |
| LB+Y | Summarize | "Summarize briefly. Ultrathink " |
| LB+D-Left | Prev window | Cmd+Shift+` |
| LB+D-Right | Next window | Cmd+` |

### RB+ Layer (Execution/Action)

| Combo | Action | Phrase/Key |
|-------|--------|------------|
| RB tap | Subagent | "Put a subagent on researching this thoroughly. Report back with findings. Ultrathink " |
| RB+A | CC prompt 1 | Key "1" (allow) |
| RB+B | CC prompt 2 | Key "2" (allow + remember) |
| RB+X | CC prompt 3 | Key "3" (custom response) |
| RB+Y | Git sync | "Pull and push. Ultrathink " |

### Action Count

| Before | After |
|--------|-------|
| 12 standalone actions | 12 standalone + 10 combos = **22 actions** |

### Testing Notes

**TODO**: Verify LB+D-pad window switching works correctly. The `grave_accent_and_tilde` key code may have ISO keyboard (Svorak) issues - same key that was problematic for keyboard Cmd+`.

### Design Principles Applied

1. **Semantic Grouping**: LB = comprehension/investigation, RB = action/execution
2. **CC Prompt Navigation**: RB+A/B/X maps to 1/2/3 for quick permission responses
3. **Couch Mode**: LB+D-pad enables window switching without keyboard
4. **Complementarity**: Combos fill gaps, not duplicate existing shortcuts
5. **Spatial Mnemonics**: A (bottom) = primary action, Y (top) = meta/overview, X/B = secondary
6. **Trailing Space**: All outputs end with space for composability
7. **Ultrathink by Default**: Include in all phrases (78% of user messages use it)

### JSON Pattern Reference

```json
{
    "description": "LB as modifier (button7)",
    "manipulators": [
        {
            "type": "basic",
            "from": { "pointing_button": "button7" },
            "to": [{
                "set_variable": { "name": "lb_held", "value": 1 }
            }],
            "to_after_key_up": [{
                "set_variable": { "name": "lb_held", "value": 0 }
            }],
            "to_if_alone": [{
                "shell_command": "osascript ... current LB action ..."
            }],
            "conditions": [{ "type": "device_if", "identifiers": [...] }]
        },
        {
            "type": "basic",
            "description": "LB + A → Combo action",
            "from": { "pointing_button": "button1" },
            "to": [{
                "shell_command": "osascript ... LB+A action ..."
            }],
            "conditions": [
                { "type": "variable_if", "name": "lb_held", "value": 1 },
                { "type": "device_if", "identifiers": [...] }
            ]
        }
    ]
}
```

### Related Resources

- Karabiner virtual modifier docs: https://karabiner-elements.pqrs.org/docs/json/extra/virtual-modifier/
- Project analysis: `QUALITATIVE_ANALYSIS.md`, `KEYBOARD_SHORTCUTS_REPORT.md`
- Existing keyboard pattern: `mods/keyboard_text_shortcuts.json` (Caps Lock modifier)

---

## Analog Stick Mapping (Word Navigation)

### The Goal
Use analog stick directional movement for word-by-word cursor navigation (Opt+Left/Right arrows).

### Karabiner Limitation
**Karabiner-Elements does not support analog stick → keyboard mapping.**

The "XY stick" settings in Karabiner's Devices → Gamepad dialog are for **mouse cursor movement only**:
- The formulas (`cos(radian) * m`, `sin(radian) * m`) convert stick position to X/Y mouse movement
- Settings like deadzone, delta magnitude, continued movement interval affect mouse cursor behavior
- **Cannot output keyboard keys** (like Opt+Left/Right for word navigation)

Karabiner only handles:
- Discrete button events (`pointing_button`, `generic_desktop`)
- Stick-to-mouse cursor conversion (via XY stick settings)

### Third-Party Solutions Required

| App | Price | Apple Silicon | Xbox Support | Notes |
|-----|-------|---------------|--------------|-------|
| **Joystick Mapper** | $4.99 | Via Rosetta 2 | ✅ Yes | **Best option** - mature, Xbox-compatible |
| **JoyKeyMapper** | Free | ✅ Native | ❌ No | Nintendo controllers only (Joy-Con, Pro) |
| **Gamepad Mapper** | $4.99 | Via Rosetta 2 | ✅ Yes | Similar to Joystick Mapper |
| **Enjoyable** | Free | ❌ No support | N/A | Abandoned (2015), doesn't work on M1/M2 |

**Winner: [Joystick Mapper](https://joystickmapper.com/)** ($4.99, one-time purchase)
- Explicitly supports Xbox controllers
- Can map analog stick directions independently
- Adjustable repeat rate per direction

### Expected Behavior
Analog sticks are treated as **threshold-based digital directions**:
- Push stick right → triggers Opt+Right repeatedly (word skip right)
- Push stick left → triggers Opt+Left repeatedly (word skip left)
- Release → stops

This is hold-to-repeat behavior, not proportional speed control.

### Coexistence with Karabiner - RISK ASSESSMENT

**Status**: Uncertain - potential HID-level conflict (December 2025)

**The Goal**: Karabiner handles buttons, Joystick Mapper handles analog sticks only.

**Why It Might Work**:
- Karabiner sees buttons as `pointing_button` events but does NOT see analog axis data
- Joystick Mapper can selectively map only specific inputs
- They intercept different input types from the same device

**Why It Might Conflict**:
- Both apps work at HID input level
- [OpenEmu wiki](https://github.com/OpenEmu/OpenEmu/wiki/Troubleshooting:-Input-problems) lists BOTH as "known problematic software" for input conflicts
- Joystick Mapper FAQ warns: "Other similar apps may prevent Joystick Mapper from operating correctly"
- HID device "grabbing" - one app might claim exclusive access

**Recommended Test Plan**:
1. Install Joystick Mapper ($4.99)
2. Configure ONLY left stick horizontal axis → Opt+Left / Opt+Right
3. Test if Karabiner button mappings (A, B, X, Y, etc.) still work
4. If conflict: Consider migrating ALL Xbox mappings to Joystick Mapper

**Fallback Option**: If coexistence fails, Joystick Mapper can handle both buttons AND sticks - could replace Karabiner for Xbox controller entirely (keep Karabiner for keyboard shortcuts only).
