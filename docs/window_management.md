# Window Management on macOS

> **Purpose**: Enable efficient window/space/app switching for both keyboard and Xbox controller use
> **Use Case**: "Couch mode" - wireless controller navigation away from desk
> **Created**: December 26, 2025

---

## Current macOS Shortcuts (from System Settings)

### Mission Control
| Action | Default Shortcut | Status |
|--------|------------------|--------|
| Mission Control | Ctrl+↑ | Working |
| Application windows | Ctrl+↓ | Working |
| Show Desktop | F11 | Working |
| Move left a space | Ctrl+← | Working |
| Move right a space | Ctrl+→ | Working |
| Switch to Desktop 1-4 | Ctrl+1/2/3/4 | Disabled |

### Window Management
| Action | Default Shortcut | Status |
|--------|------------------|--------|
| Minimize | Cmd+M | Working |
| Fill | Ctrl+Option+Globe+F | Working |
| Tile Left/Right Half | Ctrl+Option+Globe+←/→ | Working |

### Keyboard Focus
| Action | Default Shortcut | Status |
|--------|------------------|--------|
| Move focus to next window | **Cmd+`** | **BROKEN** (years!) |
| Move focus to active/next window | Ctrl+F4 | Working? |
| Move focus to menu bar | Ctrl+F2 | Working |
| Move focus to Dock | Ctrl+F3 | Working |

---

## THE PROBLEM: "Move focus to next window" (Cmd+`)

### Symptoms
- Shortcut mapped to Cmd+` in System Settings → Keyboard → Keyboard Shortcuts
- Pressing Cmd+` does nothing
- Has been broken for **years** with Svorak A6 layout
- Extremely frustrating - this is THE standard macOS shortcut for cycling windows within an app

### Root Cause Analysis

**The Backtick Key Problem on Non-US Keyboards:**

On US ANSI keyboards:
- The ` (grave accent/backtick) key is top-left, below Escape
- Physical key sends `key_code: grave_accent_and_tilde`

On Swedish ISO keyboards:
- That physical position has the § (section) key instead
- Physical key sends `key_code: non_us_backslash`
- The actual ` character is accessed via Shift+´ (acute accent) or a dead key

On Svorak A6 (Swedish Dvorak variant):
- Layout remaps further complicate which physical key produces `
- Karabiner may be intercepting or modifying the key before macOS sees it

**Why It Doesn't Work:**
1. macOS expects `Cmd + grave_accent_and_tilde` key_code
2. Your keyboard doesn't have a key that naturally sends that code
3. Karabiner may be modifying key events in a way that breaks the shortcut
4. The shortcut appears "set" but the key combination never matches

### Potential Solutions

#### Solution 1: Remap in System Settings (Easiest)
Change "Move focus to next window" to a different shortcut that works with your layout:
- `Cmd+<` (less-than, easily reachable on Svorak)
- `Ctrl+Tab` (if not conflicting with app-specific shortcuts)
- `Cmd+F1` (function key)

**How**: System Settings → Keyboard → Keyboard Shortcuts → Keyboard → "Move focus to next window" → double-click → press new keys

#### Solution 2: Karabiner Mapping (More Powerful)
Map a comfortable key combo to send `grave_accent_and_tilde`:

```json
{
    "description": "Cmd+< → Cmd+` (Move focus to next window)",
    "type": "basic",
    "from": {
        "key_code": "comma",
        "modifiers": {
            "mandatory": ["command"],
            "optional": ["any"]
        }
    },
    "to": [{
        "key_code": "grave_accent_and_tilde",
        "modifiers": ["command"]
    }]
}
```

#### Solution 3: Caps Lock Shortcut (Fits Existing Pattern)
Add to keyboard_text_shortcuts.json:
- `Caps+Tab` → Cmd+` (next window same app)
- `Caps+Shift+Tab` → Cmd+Shift+` (previous window same app)

#### Solution 4: Xbox Controller Mapping
Map a button combo to window cycling:
- `LB+D-pad Left/Right` → Cmd+`/Cmd+Shift+` (cycle windows)

---

## Couch Mode: Xbox Controller Navigation

### The Vision
Sit on couch with wireless Xbox controller, navigate macOS without keyboard/mouse for common tasks:
- Switch between Spaces (virtual desktops)
- Cycle windows within current app (Ghostty, Zed)
- Switch to browser, reload, scroll
- Basic text input via dictation (DICT button already mapped)

### Proposed Xbox Mappings for Navigation

#### Global Navigation (No Modifier)
| Button | Action | macOS Shortcut |
|--------|--------|----------------|
| D-pad Left | (current: Delete Word) | Keep as-is |
| D-pad Right | (current: Enter) | Keep as-is |
| D-pad Up | Move left a space | Ctrl+← |
| D-pad Down | Move right a space | Ctrl+→ |

**Note**: D-pad Up/Down are documented as unreliable. Test before committing.

#### LB+ Navigation Layer (Research: Look Around)
| Combo | Action | macOS Shortcut |
|-------|--------|----------------|
| LB+D-pad Left | Previous window (same app) | Cmd+Shift+` |
| LB+D-pad Right | Next window (same app) | Cmd+` |
| LB+D-pad Up | Mission Control | Ctrl+↑ |
| LB+D-pad Down | Application windows | Ctrl+↓ |

#### RB+ Action Layer (Execute: Do Things)
| Combo | Action | Notes |
|-------|--------|-------|
| RB+D-pad Left | Switch to Ghostty | AppleScript `activate` |
| RB+D-pad Right | Switch to Chrome | AppleScript `activate` |
| RB+D-pad Up | Reload browser | Cmd+R (when Chrome focused) |
| RB+D-pad Down | Switch to Zed | AppleScript `activate` |

### App-Specific Mappings

**Yes, Karabiner supports app-specific conditions!**

```json
"conditions": [
    {
        "type": "frontmost_application_if",
        "bundle_identifiers": ["com.google.Chrome"]
    }
]
```

Useful bundle identifiers:
- Ghostty: `com.mitchellh.ghostty`
- Zed: `dev.zed.Zed`
- Chrome: `com.google.Chrome`
- Safari: `com.apple.Safari`
- Cursor: `com.todesktop.230313mzl4w4u92`

### Alternative Approaches

#### Hammerspoon Integration
If Karabiner proves insufficient, Hammerspoon can:
- Respond to hotkeys with Lua scripts
- Use window management APIs directly
- Focus specific apps by name
- Move/resize windows programmatically

Location: `~/.hammerspoon/init.lua`

#### Third-Party Window Managers
- **Rectangle**: Free, keyboard-driven window management
- **Raycast**: Spotlight replacement with window commands
- **Magnet**: Paid, simple window snapping

---

## Implementation Checklist

### Phase 1: Fix "Move focus to next window"
- [ ] Test Solution 1: Remap in System Settings to Cmd+<
- [ ] If fails, try Solution 2: Karabiner mapping
- [ ] If works, add matching Xbox controller combo

### Phase 2: Basic Couch Navigation
- [ ] Test D-pad Up/Down reliability for Space switching
- [ ] If reliable, add Ctrl+←/→ mappings
- [ ] Add LB+D-pad for window cycling

### Phase 3: App Switching
- [ ] Create AppleScript commands for app activation
- [ ] Map to RB+D-pad combos
- [ ] Test app-specific conditions

### Phase 4: Polish
- [ ] Document all new mappings in xbox_button_reference.md
- [ ] Update cheatsheet generator
- [ ] Regenerate cheatsheet image

---

## Related Files

- `mods/keyboard_text_shortcuts.json` - Keyboard shortcuts (add Caps+Tab?)
- `mods/xbox_zed_claude.json` - Xbox controller mappings
- `docs/xbox_button_reference.md` - Controller documentation
- `~/.hammerspoon/init.lua` - Hammerspoon config (if needed)

---

## Questions to Resolve

1. **D-pad Up/Down reliability**: Previously documented as unreliable. Worth re-testing?
2. **Space switching frequency**: How often do you switch Spaces vs cycle windows?
3. **App switching priority**: Which apps need quick access? (Ghostty, Zed, Chrome, ?)
4. **Scroll in browser**: How to scroll without mouse? (Page Up/Down via buttons?)
