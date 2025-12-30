# TODO

> **Session resumed December 31, 2025** - Continued from Dec 20 session.
> Major progress on DICT button, cheatsheet generation, and documentation.

> **Context from Dec 20**: Last activity before that was September 8, 2025 (~3.5 months gap).
> Extensive development environment work done in ~/dotfiles during this time, including:
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

14. **DICT Button Delayed Space** *(Dec 31, 2025)*
    - [x] Identified issue: SuperWhisper transcription async, spaces not appearing between dictation and shortcuts
    - [x] Tried multiple approaches: prefix space, left-arrow, delete_forward
    - [x] Final solution: 1-second delayed clipboard+paste space (same pattern as working shortcuts)
    - [ ] **TEST**: Verify delayed space works with SuperWhisper transcription

15. **Cheatsheet Generation Improvements** *(Dec 31, 2025)* ✅ FIXED
    - [x] Fixed escaped apostrophe regex (ä showing "Let'" instead of full text)
    - [x] Removed brackets from key badges (show "u" not "[u]")
    - [x] Removed [MODIFIER] tags from Xbox cheatsheet
    - [x] Fixed DICT button not appearing (was filtered as "modifier")
    - [x] Added explicit controller layout positions for AI accuracy
    - [x] Created `docs/gemini_image_prompt_guide.md` with Google's best practices
    - [ ] **TEST**: Verify L-Stick and Guide button positions are correct in new cheatsheet

11. **Xbox Controller Modifier Combos** *(Dec 2025)* ✅ IMPLEMENTED
    - [x] Discovered: Xbox buttons CAN be used as modifiers (LB+A, RB+B, etc.)
    - [x] Documented in `docs/xbox_button_reference.md` → "Button Modifier Combos" section
    - [x] Ran `/analyze-shortcuts` with ~5,000 message history (Dec 28)
    - [x] Identified semantic groupings: LB = Exploration/Comprehension, RB = Execution/Action
    - [x] Implemented 10 combo actions:
      - **LB+ layer**: A=ZoomOut, B=Research, X=Fix, Y=Summarize, D-Left=PrevWin, D-Right=NextWin
      - **RB+ layer**: A=Key1, B=Key2, X=Key3 (CC prompts), Y=PullPush
    - [x] JSON implemented with `set_variable`/`variable_if` pattern
    - [ ] **TEST**: Verify all combos work as expected

12. **Window Management & Couch Mode** *(Dec 2025)*
    - [x] Created `docs/window_management.md` with full analysis
    - [x] Added LB+D-pad Left/Right for window switching (Cmd+Shift+`/Cmd+`)
    - [ ] **TEST**: LB+D-pad window switching may have ISO keyboard issue
      - Uses `grave_accent_and_tilde` key code - same key that's problematic for keyboard Cmd+`
      - If it doesn't work, may need to remap in System Settings OR use different key_code
    - [ ] Test D-pad Up/Down reliability (skip for now - known unreliable)
    - [ ] Consider Hammerspoon integration for complex window management

13. **Keyboard Text Shortcuts** *(Dec 2025)* - **31 shortcuts total**
    - [x] Create `keyboard_text_shortcuts.json` for typing common prompts
    - [x] Add Caps Lock dual-purpose: tap=Escape, hold+key=text shortcuts
    - [x] Handle Svorak 6 layout (map to QWERTY physical keys)
    - [x] **All Svorak keys now mapped** (Dec 28, 2025)
    - [x] Fixed spacing bug (switched from AppleScript to native `text` field)
    - [x] Added safety: Caps+Enter → Shift+Enter
    - [x] Final 3 shortcuts added (Dec 28): Caps+. (pull+push), Caps+v (research), Caps+z (/total-recap)
    - [ ] Test all shortcuts in Ghostty/Zed

    **Full mapping**: See `docs/cheatsheet_keyboard.png` and `docs/cheatsheet_xbox.png` for visual reference

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