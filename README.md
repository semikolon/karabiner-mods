# Karabiner Mods for macOS Development Workflows

> **Last updated:** January 10, 2026

## Overview
This repository contains Karabiner-Elements configurations for supercharging development workflows on macOS. Originally focused on Xbox Wireless Controller mappings, it now also includes **keyboard text shortcuts** for AI-assisted development. The ultimate goal is to streamline and possibly minimize keyboard usage by mapping various controller inputs to shortcuts, shell scripts, or macros that control or automate typical tasks in IDEs like [Cursor](https://www.cursor.so/) and terminals like [Warp](https://www.warp.dev/). By integrating these configurations with Karabiner-Elements, we can remap controller inputs to keyboard events, scripts, or application launches.

## Inspiration & Objectives
- **Reduced Keyboard Dependency**: Use the controller for common tasks such as triggering dictation (e.g., Ctrl+Ctrl), launching frequently used applications, or sending common AI prompts to Cursor.
- **Advanced Complex Modifications**: Harness Karabiner-Elements' capabilities for detecting, intercepting, and transforming inputs through JSON-based "Complex Modifications."  
- **Symlinks for Organization**: Place all your `.json` configs in this project directory, manage them here, and symlink them into Karabiner's `~/.config/karabiner/assets/complex_modifications/` folder. This can conveniently enable/disable different mods by adding or removing symlinks.
- **Trigger Shell Commands and Scripts**: Create rules that fire off shell commands. For example, focusing on a specific application window (like Cursor's chat area) and then typing a preset string. These shell scripts could also do creative tasks like capturing screenshots, calling external APIs, or integrating with other AI services.

## Potential Use Cases
1. **Developer Workflow**  
   - Jumping to definitions, toggling keyboard shortcuts, or quickly accessing terminal commands in Warp.  
   - Dictation triggers to easily switch to voice input.  
   - Launching or focusing commonly used apps (e.g., web browser, Slack, or any other commonly accessed utility).

2. **AI Conversation Management**  
   - Pre-filled prompts for AI actions: "Now let's go update the TODO.md," "Explain this code thoroughly," or "Generate tests for this function."  
   - A button dedicated to typical communication like "Alright, great work!" or "Let's think this one through in detail."

3. **Automation & Macros**  
   - Use Karabiner-Elements "Complex Modifications" alongside small shell scripts for tasks like:  
     - Taking a screenshot and pasting it into a conversation.  
     - Sending an HTTP request to a local or remote API for extra processing.  
     - Opening or creating specific files in your IDE.  

4. **Analog Inputs / Sticks**  
   - Map left or right sticks to scrolling or navigating large code files.  
   - Adjust dead zone thresholds to suit your analog preferences.

## File Structure
- **`README.md` (this file)** - Comprehensive documentation
- **`TODO.md`** - Task list and roadmap
- **`mods/`** - All Karabiner JSON complex modification files
- **`activated/`** - Symlinks to enabled mods (legacy, some mods symlinked directly)

### Available Mods

| File | Description |
|------|-------------|
| `keyboard_text_shortcuts.json` | Caps+key shortcuts for typing common text (31 shortcuts) |
| `xbox_zed_claude.json` | Xbox controller mappings - all in one rule (25 unique actions) |
| `app_specific_actions.json` | *(deprecated)* Old Cursor-specific Xbox mappings |
| `mouse_browser_navigation.json` | *(broken)* Mouse buttons for browser back/forward |
| `mouse_safari_navigation.json` | *(broken)* Safari-specific mouse navigation |

---

## Keyboard Text Shortcuts (December 2025)

Quick keyboard shortcuts for typing common AI prompts and commands in Claude Code.

### Caps Lock Dual-Purpose Design

The Caps Lock key serves two purposes:
- **Tap alone** → Escape (for vim-style workflow)
- **Hold + letter** → Type text shortcut

### Current Shortcuts

#### Tier 1: Quick Responses

| Shortcut | Output | Svorak Key | QWERTY Physical |
|----------|--------|------------|-----------------|
| **Caps+u** | `Ultrathink` | u | f |
| **Caps+p** | `Proceed. Ultrathink` | p | r |
| **Caps+s** | `Sit rep. Ultrathink` | s | ; |
| **Caps+g** | `What's the git state? Ultrathink` | g | u |

#### Tier 2: Workflow Patterns

| Shortcut | Output | Svorak Key | QWERTY Physical |
|----------|--------|------------|-----------------|
| **Caps+d** | `Make sure key docs are up to date and congruent with our progress/reasoning. Ultrathink` | d | h |
| **Caps+e** | `Don't make changes. Explore and report back. Ultrathink` | e | d |
| **Caps+a** | `Put a subagent on researching this thoroughly. Report back with findings. Ultrathink` | a | a |

#### Tier 3: Composable Doc Workflow (Jan 10, 2026)

| Shortcut | Output | Svorak Key | QWERTY Physical |
|----------|--------|------------|-----------------|
| **Caps+r** | `List 30 recent .md docs related to this work/topic. Ultrathink` | r | o |
| **Caps+c** | `Read the most relevant 2-3 ones. Ultrathink` | c | i |
| **Caps+j** | `Document insights where appropriate. Ultrathink` | j | c |
| **Caps+y** | `Why are we going down this road? Examine and challenge assumptions. Ultrathink` | y | t |

> **Note**: This keyboard uses **Svorak 6** (Swedish Dvorak) layout. Karabiner uses QWERTY physical key codes, so the JSON file maps to the physical key positions, not the letters shown on keycaps.

### Setup

1. The mod is symlinked to `~/.config/karabiner/assets/complex_modifications/`
2. Open **Karabiner-Elements** → **Complex Modifications**
3. Click **"Add rule"** → Find **"Keyboard Text Shortcuts"**
4. Enable **"Caps Lock dual-purpose: tap=Escape, hold+key=text shortcuts"**

### Troubleshooting: Svorak Layout

If shortcuts type wrong characters, the JSON may have incorrect QWERTY physical key codes. Use **Karabiner-EventViewer** to see what physical key code is being sent when you press a key.

Svorak to QWERTY physical key mapping (home row):
```
Svorak: a o e u i d h t n s
QWERTY: a s d f g h j k l ;
```

Svorak to QWERTY physical key mapping (top row):
```
Svorak: å ä ö p y f g c r l
QWERTY: q w e r t y u i o p
```

### Integration with ~/dotfiles

This repo complements the broader development environment in `~/dotfiles`:
- **Hammerspoon** (`~/.hammerspoon/`) - TTS hotkeys (Ctrl+Cmd+Alt+N/S), could host keyboard text shortcuts as fallback
- **Slash commands** (`~/.claude/commands/`) - `/total-recap`, `/docs-review`, `/significance` - potential future shortcuts
- **TTS daemon** - Audio narration system that could be triggered via controller

## How to Use
1. **Clone or Download** this repository.  
2. **Symlink JSON Files**:  
   - Place your `.json` files in the `activated` folder (to keep them organized).  
   - Create symlinks in `~/.config/karabiner/assets/complex_modifications/`.  
3. **Enable in Karabiner-Elements**:  
   - Launch Karabiner-Elements.  
   - Open the "Complex Modifications" tab → click "Add rule".  
   - Enable the relevant modifications from your new `.json` files.  
4. **Iterate & Refine**:
   - Test your mappings, gather feedback, and tweak them to fit your workflow.

> **⚠️ Reloading after edits**: Karabiner does NOT auto-reload complex modifications when JSON files change. After editing, you must manually remove the rule(s) and re-add them from the file.

## References
- **Karabiner-Elements Official Docs**:  
  [https://karabiner-elements.pqrs.org/docs/](https://karabiner-elements.pqrs.org/docs/)  
  Learn more about writing JSON for Complex Modifications.
- **Cursor**:  
  [https://www.cursor.so/](https://www.cursor.so/)  
  An AI-powered IDE where you can leverage quick prompts and macros to boost productivity.
- **Warp**:  
  [https://www.warp.dev/](https://www.warp.dev/)  
  AI-assisted terminal with advanced functionality and speed.

## Future Vision
We ultimately want an environment where the Xbox Wireless Controller can facilitate deeper synergy with AI-driven code generation, project management, and system automation—reducing friction during coding sessions and enabling partial or occasionally near-complete command of your workstation using the controller alone.

---

## Additional Controller Mappings

> **📋 Complete Reference**: See [`docs/xbox_button_reference.md`](docs/xbox_button_reference.md) for the definitive mapping between physical labels, button descriptions, and Karabiner codes.

### Physical Labels on Controller

| Label | Physical Button | Karabiner Code | Intended Action |
|-------|-----------------|----------------|-----------------|
| **ENTER** | Left Stick Click | button14 | Confirm/submit |
| **YES** | View (⧉ two windows) | button11 | Quick affirmation |
| **DICT** | Menu (☰ three lines) | button12 | Dictation toggle |
| **NO** | Guide (Xbox logo) | button13 | Cancel/escape |
| **SPECS** | B (red) | button2 | Status report |
| **STANDUP** | A (green) | button1 | Progress check |
| **<** / **>** | D-pad Left/Right | *unreliable* | Navigation |

### Reliable/Usable Buttons
1. **A Button**: button1  
2. **B Button**: button2  
3. **X Button**: button4  
4. **Y Button**: button5  
5. **View Button (Left Tiny Button)**: button11  
6. **Menu Button (Right Tiny Button)**: button12  
7. **LB (Left Bumper)**: button7  
8. **RB (Right Bumper)**: button8
9. **Guide Button (Glowing X)**: button13 (requires firmer press)
10. **Left Stick Click**: button14 (press down on left stick)
11. **Right Stick Click**: button15 (press down on right stick)

### Unreliable/Unmappable Inputs
- The D-pad does not reliably report directional presses.  
- Pressing "Up" frequently registers as "Right," and sometimes multiple directions fire simultaneously.  
- The Share button is reserved by macOS system settings and cannot be mapped in Karabiner.
- The LT/RT triggers are not detectable by Karabiner-EventViewer and cannot be mapped.
- Decision: The D-pad will not be mapped to any critical workflows.

### Goals for Joystick Remapping
- **Left Joystick**  
  - Vertical movement: map to vertical scrolling in Cursor or other apps.  
  - Horizontal movement: to be decided, but potentially mappable to specific actions.
- **Right Joystick**  
  - Horizontal movement: map to horizontal scrolling in Cursor.  
  - Vertical movement: optional or reserved for additional workflows.

### Additional Notes
- **Analog Thresholds**: Implement dead zones and step sizes to avoid jitter or micro-movements.  
- **EventViewer Usage**: Confirm all button IDs and axes in Karabiner-EventViewer before finalizing JSON.  
- **Application-Specific Conditions**: Restrict certain mappings to Cursor's window, if desired, so they don't interfere system-wide.  
- **Future Expansion**: Consider triggers (LT/RT), more advanced macros, and external AI integration.

## Personal Vision & Examples
I'd like to use this Xbox Wireless Controller to supercharge my development workflow—especially in AI-amped tools like Cursor (IDE) and Warp (terminal). Sometimes, I just want an alternative interface to direct an AI to write code or orchestrate tasks, without switching to my keyboard as often. For instance, I might press a button to:

- Trigger dictation instead of reaching for Ctrl+Ctrl.
- Quickly send a friendly note to the AI, like: "Alrighty, great work! Now let's go update the TODO.md and plan our next steps."  
- Request more in-depth reasoning: "Let's think through this problem out loud. Go through the logic behind it in detail."  
- Ensure our code is fully tested: "Let's make sure this code is well tested. Check for existing tests or generate new ones."

Over time, I can iterate on these mappings so that I can practically sit with my game controller, orchestrating AI-driven development from my couch—though I'll still hop on the keyboard whenever needed. The goal is to inch closer to a fluid, mind-melded workflow that reduces friction and fosters creativity in coding.

## Base Controller Configuration

### Stick Settings
- **Left Stick**: Controls mouse cursor movement (default Karabiner behavior)
- **Right Stick**: Controls scrolling (default Karabiner behavior)

### Stick Parameters
- Deadzone: 0.0 (reduced from default 0.10)
- Delta magnitude detection: 0.01 (reduced from default 0.02)
- Movement magnitude threshold: 0.1 (reduced from default 1.00)
- Movement interval: 10ms

These base settings provide the foundation upon which our Complex Modifications are built. The reduced thresholds allow for more precise control but may make the sticks more sensitive to small movements.

## Current Button Mappings

### Cursor-Specific Actions (mods/app_specific_actions.json)
All these mappings only trigger when Cursor is the active application.

1. **Navigation**
   - **X Button (button4)**: Focus editor (Escape) then navigate to previous change (Option+K)
   - **Y Button (button5)**: Focus editor (Escape) then navigate to next change (Option+J)
   - **D-pad Left**: Focus editor (Escape) then navigate to previous file with edits (Option+H)
   - **D-pad Right**: Focus editor (Escape) then navigate to next file with edits (Option+L)
   - **LB Button (button7)**: Switch to previous tab (Cmd+Alt+Left)
   - **RB Button (button8)**: Switch to next tab (Cmd+Alt+Right)

2. **Quick Commands**
   - **A Button (button1)**: Focus composer (Escape → Cmd+I), type "STANDUP", accept (Cmd+Enter)
   - **B Button (button2)**: Focus composer (Escape → Cmd+I), type "SPECS", accept (Cmd+Enter)
   - **View Button (button11)**: Focus composer (Escape → Cmd+I), accept (Cmd+Enter)
   - **Guide Button (button13)**: Focus composer (Escape → Cmd+I), cancel generation (Cmd+Backspace)
   - **Left Stick Click (button14)**: Send Enter in composer (without Cmd modifier)

### Global Actions
These mappings work in any application (now all in `mods/xbox_zed_claude.json`).

1. **Dictation (Menu/DICT Button)**
   - **Menu Button (button12)**: Toggle SuperWhisper on/off with automatic trailing space
   - First press: Starts dictation (sends `non_us_backslash` for ISO keyboard)
   - Second press: Ends dictation + adds 1-second delayed space via clipboard+paste
   - This ensures dictated text is separated from subsequent shortcuts

### Zed-Specific Actions (mods/xbox_zed_claude.json)
All these mappings only trigger when Zed is the active application.

1. **Claude Code Integration**
   - **A Button (button1)**: Type "/docs-review" command and execute
   - **B Button (button2)**: Type "/total-recap" command and execute
   - **Y Button (button5)**: Open Agent Panel (Cmd+?)
   - **View Button (button11)**: Accept Claude Code suggestion (Enter)

2. **Navigation & Search**
   - **X Button (button4)**: Open Command Palette (Cmd+Shift+P)
   - **LB Button (button7)**: Previous Tab (Cmd+Shift+[)
   - **RB Button (button8)**: Next Tab (Cmd+Shift+])
   - **Left Stick Click (button14)**: Search Project (Cmd+Shift+F)
   - **Right Stick Click (button15)**: Find Symbol (Cmd+T)

3. **Utility**
   - **Guide Button (button13)**: Cancel/Escape
   - **Menu Button (button12)**: SuperWhisper Global Dictation (backtick/grave key)

## Implementation Learnings

1. **Composer Focus Strategy**
   - Cmd+I toggles the composer visibility
   - To ensure consistent behavior, we first send Escape (to focus editor) then Cmd+I (to show composer)
   - For actions that might start from dictation mode (like View button or Menu button), we send Escape twice:
     - First Escape cancels any active dictation
     - Second Escape ensures editor focus
   - This sequence guarantees the composer becomes visible rather than toggling on/off

2. **Sequential Key Events**
   - Multiple "to" actions in Karabiner's JSON might not guarantee sequential execution
   - Using AppleScript with explicit delays ensures reliable sequencing:
     ```json
     "shell_command": "osascript -e 'tell application \"System Events\"' -e 'key code 53' -e 'delay 0.1' -e 'keystroke \"i\" using command down' -e 'delay 0.2' ..."
     ```

3. **Context Awareness**
   - Different shortcuts have different behaviors based on focus:
     - Option+K/J: Navigates changes in editor, types special chars in composer
     - Cmd+Enter: Accepts all changes in composer, accepts current file in editor
   - Solution: Ensure correct focus before sending shortcuts

4. **Bundle Identifier**
   - Cursor's bundle identifier: `com.todesktop.230313mzl4w4u92`
   - Used in `frontmost_application_if` conditions to make mappings Cursor-specific

## Future Possibilities

1. **Button Remapping Plans**
   - Move cancel function from LB to Guide Button (button13) for better ergonomics
   - Map LB/RB for tab/file switching in Cursor - considering two options:
     1. Open Tabs Switching (Cmd+Alt+Left/Right): Cycles through currently open tabs in order
     2. Editor History (Ctrl+- / Ctrl+Shift+-): Navigates through recently visited locations
   - Explore potential uses for newly discovered stick clicks (button14/15)

2. **Joystick Integration**
   - Right stick already controls scrolling when editor is focused
   - Investigate and optimize left stick movement delay
   - Fine-tune deadzone and movement parameters for optimal control

3. **Additional Commands**
   - More preset AI prompts could be mapped to unused buttons
   - Could add Warp-specific actions for the same buttons
   - Consider mapping common VS Code actions since Cursor inherits its shortcuts

## Technical Notes

1. **File Organization**
   - Mods stored in `mods/*.json`
   - Symlinked through `activated/` to Karabiner's complex modifications directory
   - Enables easy enabling/disabling of specific mods

2. **AppleScript Usage**
   - Used for reliable sequential key events
   - Allows precise timing control with delays
   - Example:
     ```applescript
     tell application "System Events"
         key code 53                     # Escape
         delay 0.1
         keystroke "i" using command down # Cmd+I
         delay 0.2
         # ... additional commands
     end tell
     ```

3. **Keyboard Layout Considerations**
   - Our mappings currently assume a US keyboard layout
   - Option+K/J navigation might need alternatives for different layouts
   - Consider documenting alternative mappings for common layouts

4. **Context-Sensitive Actions**
   - Our focus-first approach (Escape → Cmd+I) aligns with industry practices
   - VS Code's `when` clause pattern validates our need for context-awareness
   - Future mappings could consider:
     - File type specific actions
     - Editor state awareness
     - Different behaviors based on cursor position

5. **Command Composition**
   - Our AppleScript sequences mirror VS Code's command argument pattern
   - Both approaches solve the need to bundle multiple actions
   - AppleScript gives us more control over timing and sequencing
