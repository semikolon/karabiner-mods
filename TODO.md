# TODO

> **Session resumed December 20, 2025** - Last activity was September 8, 2025 (~3.5 months ago).
> Context: Extensive development environment work done in ~/dotfiles during this time, including:
> - TTS daemon with Hammerspoon hotkeys (Ctrl+Cmd+Alt+N/S)
> - Rich slash command ecosystem (`/total-recap`, `/docs-review`, `/significance`, etc.)
> - MCP server integrations (Zen, Graphiti, Serena, Linear, etc.)
> 
> **Integration opportunities identified:**
> - Hammerspoon as fallback for keyboard shortcuts (if Fn key doesn't work via Karabiner)
> - Text shortcuts for common AI prompts (Ultrathink, slash commands)
> - Potential synergy between Karabiner controller mappings and Hammerspoon hotkeys

---

## Active / Recent

11. **Keyboard Text Shortcuts** *(Dec 2025)*
    - [x] Create `keyboard_text_shortcuts.json` for typing common prompts
    - [x] Add Caps Lock dual-purpose: tap=Escape, hold+key=text shortcuts
    - [x] Handle Svorak 6 layout (map to QWERTY physical keys)
    - [x] **Tier 1 shortcuts implemented:**
      - Caps+u → "Ultrathink"
      - Caps+c → "Continue. Ultrathink"
      - Caps+y → "Yes! Ultrathink"
      - Caps+p → "Proceed. Ultrathink"
      - Caps+s → "Sit rep. Ultrathink"
      - Caps+g → "What's the git state? Ultrathink"
    - [x] **Tier 2 shortcuts implemented** (Dec 21, 2025):
      - Caps+d → "Make sure key docs are up to date and congruent with our progress. Ultrathink"
      - Caps+e → "Don't make changes. Explore and report back. Ultrathink"
      - Caps+a → "Put a subagent on researching this thoroughly. Report back with findings. Ultrathink"
    - [x] Fixed spacing bug (switched from AppleScript to native `text` field)
    - [ ] Test all shortcuts in Ghostty/Zed
    
    **Analysis reports created:**
    - `KEYBOARD_SHORTCUTS_REPORT.md` - Quantitative analysis (1,117 messages)
    - `QUALITATIVE_ANALYSIS.md` - Intent-based analysis and recommendations

---

## Original Roadmap

1. **Complex Mod Files**  
   - [ ] Create initial `xbox_controller.json` with basic button remaps to shortcuts that streamline Cursor usage (e.g., dictation toggles, quick AI prompts).  
   - [ ] Add more advanced manipulations for analog sticks (scrolling or multi-axis navigation).  
   - [ ] Explore synergy with media keys or function keys for quickly toggling speech-to-text or muting the system.

2. **Shell Automation**  
   - [ ] Write a shell script to auto-focus Cursor's chat area and insert a prewritten AI prompt.  
   - [ ] Integrate advanced tasks such as capturing a screenshot and automatically attaching it to the chat.  
   - [ ] Investigate hooking in other AI APIs that process text or code, returning results to be pasted automatically.

3. **Symlink Setup**  
   - [ ] Create a subdirectory (e.g., `activated/`) to store symlinks.  
   - [ ] Document clear steps on how to enable or disable a mod by adding/removing its symlink.

4. **Testing & Debugging**  
   - [ ] Use Karabiner-EventViewer or logs to confirm button and stick inputs are recognized.  
   - [ ] Validate that all triggers, combos, or thresholds behave as expected.

5. **Voice Control**  
   - [ ] Map a dedicated controller button to trigger macOS dictation (Ctrl+Ctrl or however configured).  
   - [ ] Optionally integrate with more advanced speech recognition tools or AI-driven dictation.

6. **User Experience Enhancements**  
   - [ ] Provide default sensitivity levels for analog sticks (dead zones, velocity thresholds).  
   - [ ] Offer multiple profiles for different contexts (e.g., "Browsing," "Coding," "Testing").

7. **Documentation**  
   - [ ] Keep the `README.md` updated with any new or changed capabilities.  
   - [ ] Provide usage examples (video demonstrations or animated GIFs could help).  

8. **Refine Reliable vs. Unreliable Buttons**
   - [x] Prioritize "button1," "button2," "button4," "button5," "button7," "button8," "button11," and "button12" for key tasks in Cursor and Warp.
   - [x] Explicitly exclude the D-pad from critical mappings given its inconsistent directional reporting.
   - [ ] Continue experimenting with thresholds and step sizes for joystick scrolling and navigation.
   - [ ] Test and document the newly discovered button14 (Left Stick Click) and button15 (Right Stick Click).
   - [ ] Move cancel function from LB (button7) to Guide Button (button13).
   - [ ] Test both navigation options for LB/RB mapping:
     - Open Tabs Switching (Cmd+Alt+Left/Right)
     - Editor History (Ctrl+- / Ctrl+Shift+-)
   - [ ] Map LB/RB to the most intuitive navigation method based on testing.

9. **Automate Common AI Chat Tasks**
   - [ ] Add JSON-based modifications or shell scripts that insert everyday AI prompts (e.g., "Alrighty, great work!") at the press of a button.
   - [ ] Consider triggers for deeper reasoning prompts or test-generation prompts without manually typing them each time.

10. **Optimize Stick Controls**
    - [ ] Fine-tune the reduced deadzone (0.0) and movement parameters for optimal control.
    - [ ] Document any issues or improvements needed with the current mouse/scroll behavior.
    - [ ] Investigate the left stick movement delay and potential solutions.

---