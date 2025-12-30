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
DICTATION_CONFIG_PATH = PROJECT_ROOT / "mods" / "dictation_toggle.json"
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
    "u": 1, "c": 1, "y": 1, "p": 1, "s": 1, "g": 1,
    "d": 2, "e": 2, "a": 2,
    "x": 3, "r": 3, "n": 3,
    "t": 4, "ö": 4,
    "w": 5, "å": 5, "f": 5, "h": 5, "j": 5, "ä": 5,
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
        text_match = re.search(
            r'set the clipboard to [\\"]+"?(.+?)[\\"]+"?\s*\'', shell_cmd
        )
        if text_match:
            output_text = text_match.group(1).replace('\\"', '"').replace("\\\\", "\\")
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


def extract_xbox_mappings(config_path: Path, dictation_path: Path) -> dict:
    """Extract Xbox controller mappings from Karabiner configs.

    Returns dict with 'standalone' and 'combos' keys for structured display.
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

    # Read main Xbox config
    with open(config_path) as f:
        config = json.load(f)

    for rule in config["rules"]:
        desc = rule.get("description", "")
        manipulator = rule["manipulators"][0]

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

        # For modifier buttons, use to_if_alone for the tap action
        if to_if_alone and "shell_command" in to_if_alone:
            shell_cmd = to_if_alone["shell_command"]
            text_match = re.search(r'set the clipboard to [\\"]+"?(.+?)[\\"]+"?\s*\'', shell_cmd)
            if text_match:
                tap_output = text_match.group(1).replace('\\"', '"').replace("\\\\", "\\").strip()
            else:
                tap_output = desc.split("→")[-1].strip() if "→" in desc else desc
        else:
            tap_output = None

        if to_action:
            if "shell_command" in to_action:
                shell_cmd = to_action["shell_command"]
                text_match = re.search(r'set the clipboard to [\\"]+"?(.+?)[\\"]+"?\s*\'', shell_cmd)
                if text_match:
                    output = text_match.group(1).replace('\\"', '"').replace("\\\\", "\\").strip()
                else:
                    output = desc.split("→")[-1].strip() if "→" in desc else desc
            elif "key_code" in to_action:
                key = to_action["key_code"]
                modifiers = to_action.get("modifiers", [])
                if modifiers:
                    output = f"[{'+'.join(modifiers)}+{key}]"
                else:
                    output = f"[{key}]"
            elif "set_variable" in to_action:
                # This is a modifier definition, use tap action
                output = tap_output or "modifier"
            else:
                output = desc
        else:
            output = desc

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
        elif "set_variable" in (to_action or {}):
            # Modifier button - add to standalone with tap action
            mapping["output"] = tap_output or "modifier"
            mapping["is_modifier"] = True
            standalone.append(mapping)
        else:
            standalone.append(mapping)

    # Read dictation config for DICT button
    if dictation_path.exists():
        with open(dictation_path) as f:
            dictation_config = json.load(f)

        for rule in dictation_config["rules"]:
            desc = rule.get("description", "")
            standalone.append({
                "button": "Menu",
                "label": "DICT",
                "output": "SuperWhisper (dictation)",
                "desc": desc,
            })

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
            content_lines.append(f"  [{s['key']}] → {output}")

    content = "\n".join(content_lines)

    return f"""Create a CLEAN, READABLE keyboard shortcut reference card.

ALL SHORTCUTS USE: Caps Lock + key (show this ONCE as a header, NOT on each line)

SHORTCUTS TO DISPLAY:
{content}

DESIGN REQUIREMENTS:

LAYOUT:
- Single column or two-column layout to fit all shortcuts
- Group shortcuts by tier/category with subtle section dividers
- Each shortcut: small key badge [x] followed by the output text
- Show as much of each phrase as possible - minimize truncation!

STYLE (minimalist synthwave):
- Background: Dark navy #1a1a2e, edge-to-edge (NO white borders/margins)
- Section headers: Coral/orange #ff8c42
- Key badges: Small, rounded, subtle border
- Text: Clean white #eaeaea, readable size

CRITICAL:
- NO white margins or borders - dark background to all edges
- Show "Caps + key" ONCE at top, not repeated on each shortcut
- Prioritize showing FULL shortcut text over decoration
- Every shortcut must be legible
- Aspect ratio: 16:10 landscape
- Resolution: 2K quality"""


def build_xbox_prompt(mappings: dict) -> str:
    """Build prompt for Xbox-only cheatsheet."""

    standalone = mappings["standalone"]
    lb_combos = mappings["lb_combos"]
    rb_combos = mappings["rb_combos"]

    # Build standalone list
    standalone_lines = []
    for m in standalone:
        label = f" ({m['label']})" if m.get("label") else ""
        modifier_note = " [MODIFIER]" if m.get("is_modifier") else ""
        output = m["output"][:60] + "..." if len(m["output"]) > 60 else m["output"]
        standalone_lines.append(f"  {m['button']}{label}{modifier_note} → {output}")

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

    return f"""Create a CLEAN Xbox controller shortcut reference card.

CONTROLLER PHYSICAL LAYOUT (for accurate button positions):
- Face buttons (RIGHT SIDE, diamond): A=bottom green, B=right red, X=left blue, Y=top yellow
- Shoulder buttons (TOP EDGE): LB=left bumper, RB=right bumper
- D-pad (LEFT SIDE): directional pad with 4 directions
- Center: View button (left), Xbox logo (center), Menu button (right)
- Analog sticks: Left stick, Right stick (both clickable)

STANDALONE BUTTON ACTIONS (press button alone):
{standalone_content}

LB+ MODIFIER COMBOS (hold LB, press button):
{lb_content}

RB+ MODIFIER COMBOS (hold RB, press button):
{rb_content}

DESIGN REQUIREMENTS:

LAYOUT (top to bottom):
1. Controller diagram at TOP - clear illustration of Xbox controller
2. Draw simple lines from buttons to their STANDALONE action labels
3. Below the diagram: Two tables side-by-side for LB+ and RB+ combos
4. Lines should be SIMPLE and ACCURATE - go to correct button positions!

CRITICAL FOR DIAGRAM:
- Lines must connect to CORRECT physical button locations
- LB/RB are shoulder buttons at TOP of controller
- A/B/X/Y are face buttons on RIGHT side in diamond pattern
- D-pad is on LEFT side
- Do NOT draw lines for modifier combos - those go in tables below

STYLE (minimalist synthwave):
- Background: Dark navy #1a1a2e, edge-to-edge (NO white borders/margins)
- Controller: Electric blue #00d4ff outline
- Section headers: Electric blue accent
- Text: Clean white #eaeaea

CRITICAL:
- NO white margins or borders - dark background to all edges
- Controller diagram is REQUIRED
- Keep lines minimal and ACCURATE
- Modifier combos in TABLES, not as diagram lines
- Aspect ratio: 16:10 landscape
- Resolution: 2K quality"""


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

    # Extract Xbox mappings (including dictation)
    print(f"Reading Xbox configs: {XBOX_CONFIG_PATH}, {DICTATION_CONFIG_PATH}")
    xbox_mappings = extract_xbox_mappings(XBOX_CONFIG_PATH, DICTATION_CONFIG_PATH)
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
