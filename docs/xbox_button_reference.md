# Xbox Controller Button Reference

> **Purpose**: Definitive mapping between physical controller buttons, their labels, and Karabiner codes.
>
> **Controller**: Xbox Wireless Controller (Vendor ID: 1118, Product ID: 2835)
> **Last Updated**: December 22, 2025

## Complete Button Mapping

| Physical Label | Physical Button | Icon/Description | Karabiner Code | Current Action |
|----------------|-----------------|------------------|----------------|----------------|
| **YES** | View Button | Two overlapping rectangles | `button11` | "Yes! Ultrathink " |
| **DICT** | Menu Button | Three horizontal lines | `button12` | SuperWhisper (non_us_backslash) |
| **NO** | Guide Button | Glowing Xbox logo | `button13` | Escape |
| **SPECS** | B Button | Red "B" on face | `button2` | "Sit rep. Ultrathink " |
| **STANDUP** | A Button | Green "A" on face | `button1` | "What's next according to the plan? Ultrathink " |
| *(unlabeled)* | X Button | Blue "X" on face | `button4` | "Read up on the relevant docs..." (context refresh) |
| *(unlabeled)* | Y Button | Yellow "Y" on face | `button5` | "Make sure key docs are up to date..." (doc check) |
| *(unlabeled)* | LB | Left Bumper | `button7` | "Don't make changes. Explore..." |
| *(unlabeled)* | RB | Right Bumper | `button8` | "Put a subagent on researching..." |
| *(unlabeled)* | D-pad Left | Left arrow on D-pad | `generic_desktop: dpad_left` | Delete Word (Opt+Backspace) |
| *(unlabeled)* | D-pad Right | Right arrow on D-pad | `generic_desktop: dpad_right` | Enter key |
| *(unlabeled)* | Left Stick Click | Press down on left joystick | `button14` | /total-recap (session recovery) |
| *(unlabeled)* | Right Stick Click | Press down on right joystick | `button15` | "Commit everything in logical groups. Then push." |

## Visual Layout

```
                    [LB button7]              [RB button8]
                    "Explore"                 "Subagent"
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
```

## Button Categories

### Labeled Buttons (physical labels on controller)
| Label | Button | Action | Notes |
|-------|--------|--------|-------|
| YES | button11 | "Yes! Ultrathink " | Quick confirmation with thinking |
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
| `mods/xbox_zed_claude.json` | Main controller mappings (10 buttons) | **ENABLE THIS** |
| `mods/dictation_toggle.json` | DICT button (button12) only | **ENABLE THIS** |

### Deprecated/Disabled Files
| File | Purpose | Status |
|------|---------|--------|
| `mods/app_specific_actions.json` | Old Cursor-specific mappings | **DISABLE** |

**Note**: `dictation_toggle.json` and `xbox_zed_claude.json` don't conflict - dictation_toggle handles button12 exclusively, while xbox_zed_claude handles all other buttons.

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
