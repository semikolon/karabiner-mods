#!/usr/bin/env python3
"""
Generate visual cheat sheets for Karabiner keyboard and Xbox controller shortcuts.
Uses Nano Banana Pro (Gemini 3 Pro Image) for AI-generated infographics.

Generates TWO separate images for clarity:
- docs/cheatsheet_keyboard.png - Keyboard shortcuts only
- docs/cheatsheet_xbox.png - Xbox controller mappings only

Usage:
    python3 scripts/generate_cheatsheet_ai.py

Requires:
    - GEMINI_API_KEY environment variable
    - pip install google-genai pillow
"""

import json
import os
import re
from io import BytesIO
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai not installed. Install with: pip install google-genai")
    exit(1)

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow not installed. Install with: pip install pillow")
    exit(1)

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
KEYBOARD_CONFIG_PATH = PROJECT_ROOT / "mods" / "keyboard_text_shortcuts.json"
XBOX_CONFIG_PATH = PROJECT_ROOT / "mods" / "xbox_zed_claude.json"
# Note: DICT button is now merged into xbox_zed_claude.json (Dec 2025)
OUTPUT_DIR = PROJECT_ROOT / "docs"
OUTPUT_KEYBOARD = OUTPUT_DIR / "cheatsheet_keyboard.png"
OUTPUT_XBOX = OUTPUT_DIR / "cheatsheet_xbox.png"

# Tier configuration for keyboard shortcuts
KEYBOARD_TIER_NAMES = {
    1: "Quick Responses",
    2: "Workflow Patterns",
    3: "Combo Phrases",
    4: "Testing & Research",
    5: "Semantic Actions",
    6: "Slash Commands",
}

TIER_ASSIGNMENTS = {
    "u": 1, "p": 1, "s": 1, "g": 1,
    "d": 2, "e": 2, "a": 2,
    "x": 3, "r": 3, "n": 3, "c": 3,  # c is now "Read relevant 2-3"
    "t": 4, "ö": 4,
    "w": 5, "å": 5, "f": 5, "h": 5, "j": 5, "ä": 5, "y": 5,  # y is "Challenge assumptions"
    "m": 6, "k": 6, "i": 6, "b": 6, "l": 6, "o": 6, "q": 6,
    # New shortcuts
    ".": 2, "v": 4, "z": 6,
}


def extract_keyboard_shortcuts(config_path: Path) -> list[dict]:
    """Extract keyboard shortcut info from Karabiner config."""
    with open(config_path) as f:
        config = json.load(f)

    shortcuts = []
    manipulators = config["rules"][0]["manipulators"]

    for m in manipulators:
        if m["type"] != "basic":
            continue
        desc = m.get("description", "")
        if not desc.startswith("Caps+"):
            continue

        # Parse description: "Caps+u → Ultrathink (Svorak u = QWERTY f)"
        match = re.match(
            r"Caps\+(\S+)\s*→\s*(.+?)\s*\(Svorak \S+ = QWERTY (\S+)\)", desc
        )
        if not match:
            match = re.match(r"Caps\+(\S+)\s*→\s*(.+)", desc)
            if match:
                svorak_key = match.group(1)
                name = match.group(2)
            else:
                continue
        else:
            svorak_key = match.group(1)
            name = match.group(2)

        # Extract the actual text from shell command
        shell_cmd = m["to"][0].get("shell_command", "")
        # Match text between "set the clipboard to" and the next osascript command
        # Handle both "double quoted" and 'single quoted' with escaped apostrophes
        text_match = re.search(
            r'set the clipboard to [\\\'"]+(.+?)[\\\'"]+\s*-e\s', shell_cmd
        )
        if text_match:
            output_text = text_match.group(1)
            # Clean up shell escape sequences and surrounding quotes
            output_text = output_text.strip('"\'')
            output_text = output_text.replace("'\\''", "'").replace("\\'", "'").replace('\\"', '"').replace("\\\\", "\\")
            # Strip "Ultrathink" suffix for cleaner display (user knows it's always there)
            output_text = re.sub(r'\s*Ultrathink\s*$', '', output_text)
        else:
            output_text = name

        tier = TIER_ASSIGNMENTS.get(svorak_key, 1)

        shortcuts.append({
            "key": svorak_key,
            "output": output_text.strip(),
            "tier": tier,
            "tier_name": KEYBOARD_TIER_NAMES.get(tier, f"Tier {tier}"),
        })

    return sorted(shortcuts, key=lambda x: (x["tier"], x["key"]))


def extract_xbox_mappings(config_path: Path) -> dict:
    """Extract Xbox controller mappings from Karabiner config.

    Returns dict with 'standalone' and 'combos' keys for structured display.
    Note: DICT button is now included in the main xbox_zed_claude.json file.
    """
    # Button label mappings (physical labels on controller)
    BUTTON_LABELS = {
        "button1": ("A", "STANDUP"),
        "button2": ("B", "SPECS"),
        "button4": ("X", None),
        "button5": ("Y", None),
        "button7": ("LB", None),
        "button8": ("RB", None),
        "button11": ("View", "YES"),
        "button12": ("Menu", "DICT"),
        "button13": ("Guide", "NO"),
        "button14": ("L-Stick", None),
        "button15": ("R-Stick", None),
        "dpad_left": ("D-Left", None),
        "dpad_right": ("D-Right", None),
    }

    standalone = []
    lb_combos = []
    rb_combos = []
    seen_standalone_buttons = set()  # Track buttons to avoid duplicates (e.g., DICT has 2 manipulators)

    # Read main Xbox config
    with open(config_path) as f:
        config = json.load(f)

    for rule in config["rules"]:
        # Iterate over ALL manipulators in the rule (important for merged configs)
        for manipulator in rule["manipulators"]:
            desc = manipulator.get("description", "") or rule.get("description", "")

            # Get button from pointing_button or generic_desktop
            from_key = manipulator["from"]
            if "pointing_button" in from_key:
                button = from_key["pointing_button"]
            elif "generic_desktop" in from_key:
                button = from_key["generic_desktop"]
            else:
                continue

            # Check for combo vs standalone
            conditions = manipulator.get("conditions", [])
            is_lb_combo = any(c.get("name") == "lb_held" and c.get("value") == 1 for c in conditions)
            is_rb_combo = any(c.get("name") == "rb_held" and c.get("value") == 1 for c in conditions)

            # Extract output text or key action
            to_action = manipulator["to"][0] if manipulator.get("to") else None
            to_if_alone = manipulator.get("to_if_alone", [{}])[0] if manipulator.get("to_if_alone") else None

            # Human-readable key names
            KEY_NAMES = {
                "delete_or_backspace": "Backspace",
                "return_or_enter": "Enter",
                "escape": "Escape",
                "spacebar": "Space",
                "grave_accent_and_tilde": "` (backtick)",
                "non_us_backslash": "SuperWhisper",
            }

            def extract_text_from_shell(shell_cmd):
                """Extract clipboard text from shell command, handling escaped quotes."""
                text_match = re.search(r'set the clipboard to [\\\'"]+(.+?)[\\\'"]+\s*-e\s', shell_cmd)
                if text_match:
                    output = text_match.group(1).strip('"\'')
                    output = output.replace("'\\''", "'").replace("\\'", "'").replace('\\"', '"').replace("\\\\", "\\")
                    # Strip "Ultrathink" suffix for cleaner display
                    output = re.sub(r'\s*Ultrathink\s*$', '', output)
                    return output.strip()
                return None

            # For modifier buttons, use to_if_alone for the tap action
            if to_if_alone and "shell_command" in to_if_alone:
                tap_output = extract_text_from_shell(to_if_alone["shell_command"])
                if not tap_output:
                    tap_output = desc.split("→")[-1].strip() if "→" in desc else desc
            else:
                tap_output = None

            # Look through ALL actions in 'to' array, not just first
            to_actions = manipulator.get("to", [])
            output = None

            for action in to_actions:
                if "shell_command" in action:
                    extracted = extract_text_from_shell(action["shell_command"])
                    if extracted:
                        output = extracted
                        break
                elif "key_code" in action:
                    key = action["key_code"]
                    key_name = KEY_NAMES.get(key, key)
                    modifiers = action.get("modifiers", [])
                    if modifiers:
                        mod_str = "+".join(m.title() for m in modifiers)
                        output = f"{mod_str}+{key_name}"
                    else:
                        output = key_name
                    # Don't break - shell_command takes priority if found later

            # If still no output, check if it's a modifier with tap action
            if not output:
                if any("set_variable" in a for a in to_actions):
                    output = tap_output or "modifier"
                else:
                    output = desc.split("→")[-1].strip() if "→" in desc else desc

            button_info = BUTTON_LABELS.get(button, (button, None))
            button_name = button_info[0]
            label = button_info[1]

            mapping = {
                "button": button_name,
                "label": label,
                "output": output,
                "desc": desc,
            }

            if is_lb_combo:
                lb_combos.append(mapping)
            elif is_rb_combo:
                rb_combos.append(mapping)
            else:
                # Skip if we've already seen this button (e.g., DICT has start + end manipulators)
                if button_name in seen_standalone_buttons:
                    continue
                seen_standalone_buttons.add(button_name)

                # Check if this is a PURE modifier (only set_variable, no other action)
                # DICT has set_variable + key_code, so it's NOT a pure modifier
                is_pure_modifier = (
                    any("set_variable" in a for a in to_actions) and
                    not any("key_code" in a or "shell_command" in a for a in to_actions)
                )
                if is_pure_modifier:
                    mapping["output"] = tap_output or "modifier"
                    mapping["is_modifier"] = True
                standalone.append(mapping)

    # Note: DICT button is now in main config, extracted above

    return {
        "standalone": standalone,
        "lb_combos": lb_combos,
        "rb_combos": rb_combos,
    }


def build_keyboard_prompt(shortcuts: list[dict]) -> str:
    """Build prompt for keyboard-only cheatsheet."""

    # Group by tier
    tiers = {}
    for s in shortcuts:
        tier = s["tier"]
        if tier not in tiers:
            tiers[tier] = {"name": s["tier_name"], "shortcuts": []}
        tiers[tier]["shortcuts"].append(s)

    # Build content with fuller text
    content_lines = []
    for tier_num in sorted(tiers.keys()):
        tier = tiers[tier_num]
        content_lines.append(f"\n{tier['name']}:")
        for s in tier["shortcuts"]:
            # Show more text - only truncate very long ones
            output = s["output"][:80] + "..." if len(s["output"]) > 80 else s["output"]
            content_lines.append(f"  {s['key']} → {output}")

    content = "\n".join(content_lines)

    return f"""Create a CLEAN, READABLE keyboard shortcut reference card.

ALL SHORTCUTS USE: Caps Lock + key (show this ONCE as a header, NOT on each line)

SHORTCUTS TO DISPLAY (each shortcut appears EXACTLY ONCE):
{content}

DESIGN REQUIREMENTS:

LAYOUT:
- Two-column layout to fit all shortcuts
- Each category/tier appears ONLY ONCE (no duplicates!)
- Each shortcut: key letter (no brackets) in slightly larger font, followed by → and output text
- Show as much of each phrase as possible - minimize truncation!

KEY BADGE STYLE:
- Show just the letter/symbol (e.g., "u" not "[u]")
- Key letter slightly larger than description text for visual hierarchy
- Subtle rounded background or border around the key letter

STYLE (minimalist synthwave):
- Background: Dark navy #1a1a2e, edge-to-edge (NO white borders/margins)
- Section headers: Coral/orange #ff8c42
- Key letters: Slightly larger, clean styling without brackets
- Text: Clean white #eaeaea, readable size

CRITICAL:
- NO DUPLICATES - each section and shortcut appears exactly once
- NO brackets around key letters
- NO white margins or borders - dark background to all edges
- Show "Caps + key" ONCE at top, not repeated on each shortcut
- Aspect ratio: 16:10 landscape
- Resolution: 2K quality"""


def build_xbox_prompt(mappings: dict) -> str:
    """Build prompt for Xbox-only cheatsheet."""

    standalone = mappings["standalone"]
    lb_combos = mappings["lb_combos"]
    rb_combos = mappings["rb_combos"]

    # Build standalone list - skip modifier buttons (they're shown via their combos)
    standalone_lines = []
    for m in standalone:
        # Skip entries that just say "modifier" - not useful
        if m.get("output") == "modifier":
            continue
        label = f" ({m['label']})" if m.get("label") else ""
        # For modifier buttons with tap action, show as "LB (tap)" not "LB [MODIFIER]"
        if m.get("is_modifier"):
            button_display = f"{m['button']} (tap)"
        else:
            button_display = f"{m['button']}{label}"
        output = m["output"][:60] + "..." if len(m["output"]) > 60 else m["output"]
        standalone_lines.append(f"  {button_display} → {output}")

    # Build combo tables
    lb_lines = []
    for m in lb_combos:
        output = m["output"][:50] + "..." if len(m["output"]) > 50 else m["output"]
        lb_lines.append(f"  LB+{m['button']} → {output}")

    rb_lines = []
    for m in rb_combos:
        output = m["output"][:50] + "..." if len(m["output"]) > 50 else m["output"]
        rb_lines.append(f"  RB+{m['button']} → {output}")

    standalone_content = "\n".join(standalone_lines)
    lb_content = "\n".join(lb_lines)
    rb_content = "\n".join(rb_lines)

    return f"""Create an Xbox controller reference card.

LAYOUT: Controller diagram on top, two tables below.

CONTROLLER BUTTON POSITIONS (left to right):
- LEFT SIDE: LB (shoulder), L-Stick joystick (UPPER-LEFT), D-pad (LOWER-LEFT)
- CENTER THREE BUTTONS (small, in a row): View (left) | [skip middle] | Menu (right)
- RIGHT SIDE: RB (shoulder), face buttons (ABXY diamond), R-Stick joystick (LOWER-RIGHT)
- TOP CENTER: Guide button (glowing Xbox logo)

LABEL PLACEMENT RULE:
- View (YES) + Ultrathink: label on LEFT, line points to left center button
- Menu (DICT) + SuperWhisper: label on RIGHT, line points to right center button
- L-Stick, D-pad, LB labels: LEFT side
- R-Stick, face buttons (ABXY), RB labels: RIGHT side

STANDALONE BUTTON DATA:
{standalone_content}

LB COMBOS (left table):
{lb_content}

RB COMBOS (right table):
{rb_content}

STYLE: Dark navy background #1a1a2e, cyan controller outline #00d4ff, white text, 16:10 landscape.

RULES:
- Each button label appears exactly once
- Draw thin lines from buttons to their labels
- The tiny center button between View and Menu has no mapping (skip it)"""


def generate_image(prompt: str, output_path: Path, description: str) -> bool:
    """Generate an infographic using Nano Banana Pro."""

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        return False

    print(f"\nGenerating {description}...")
    print(f"Prompt length: {len(prompt)} chars")
    print("(This may take 30-60 seconds)")

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
                temperature=0.7,
            ),
        )

        # Extract image from response
        for part in response.candidates[0].content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                image_data = part.inline_data.data
                image = Image.open(BytesIO(image_data))

                output_path.parent.mkdir(parents=True, exist_ok=True)
                image.save(output_path, "PNG")
                print(f"Generated: {output_path}")
                print(f"Image size: {image.size[0]}x{image.size[1]}")
                return True

        print(f"Error: No image generated for {description}")
        return False

    except Exception as e:
        print(f"Error generating {description}: {e}")
        return False


def main():
    print("=" * 60)
    print("Karabiner Cheatsheet Generator (Nano Banana Pro)")
    print("Generating SEPARATE keyboard and Xbox cheatsheets")
    print("=" * 60)

    # Extract keyboard shortcuts
    print(f"\nReading keyboard config: {KEYBOARD_CONFIG_PATH}")
    keyboard_shortcuts = extract_keyboard_shortcuts(KEYBOARD_CONFIG_PATH)
    print(f"Found {len(keyboard_shortcuts)} keyboard shortcuts")

    # Extract Xbox mappings (DICT button now included in main config)
    print(f"Reading Xbox config: {XBOX_CONFIG_PATH}")
    xbox_mappings = extract_xbox_mappings(XBOX_CONFIG_PATH)
    total_xbox = len(xbox_mappings["standalone"]) + len(xbox_mappings["lb_combos"]) + len(xbox_mappings["rb_combos"])
    print(f"Found {total_xbox} Xbox mappings ({len(xbox_mappings['standalone'])} standalone, {len(xbox_mappings['lb_combos'])} LB+, {len(xbox_mappings['rb_combos'])} RB+)")

    # Generate keyboard cheatsheet
    keyboard_prompt = build_keyboard_prompt(keyboard_shortcuts)
    keyboard_success = generate_image(keyboard_prompt, OUTPUT_KEYBOARD, "keyboard cheatsheet")

    # Generate Xbox cheatsheet
    xbox_prompt = build_xbox_prompt(xbox_mappings)
    xbox_success = generate_image(xbox_prompt, OUTPUT_XBOX, "Xbox cheatsheet")

    print("\n" + "=" * 60)
    if keyboard_success and xbox_success:
        print("SUCCESS! Both cheatsheets generated.")
        print(f"\nOpen with:")
        print(f"  open {OUTPUT_KEYBOARD}")
        print(f"  open {OUTPUT_XBOX}")
    else:
        print("Some cheatsheets failed to generate. Check errors above.")


if __name__ == "__main__":
    main()
