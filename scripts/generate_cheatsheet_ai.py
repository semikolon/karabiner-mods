#!/usr/bin/env python3
"""
Generate a visual cheat sheet for Karabiner keyboard shortcuts using Nano Banana Pro.
(Gemini 3 Pro Image - Google's state-of-the-art infographic generation model)

Reads shortcuts from the JSON config and produces a beautiful AI-generated infographic.

Usage:
    python3 scripts/generate_cheatsheet_ai.py

Output:
    docs/cheatsheet_ai.png

Requires:
    - GEMINI_API_KEY environment variable
    - pip install google-genai pillow
"""

import base64
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
OUTPUT_DIR = PROJECT_ROOT / "docs"
OUTPUT_PNG = OUTPUT_DIR / "cheatsheet_ai.png"

# Tier configuration for keyboard shortcuts
KEYBOARD_TIER_NAMES = {
    1: "Quick Responses",
    2: "Workflow Patterns",
    3: "Combo Phrases",
    4: "Testing & Research",
    5: "Semantic Actions",
    6: "Slash Commands",
}

# Xbox controller categories
XBOX_CATEGORIES = {
    "labeled": "Labeled Buttons",
    "workflow": "Workflow Actions",
    "utility": "Utility",
}

TIER_ASSIGNMENTS = {
    "u": 1,
    "c": 1,
    "y": 1,
    "p": 1,
    "s": 1,
    "g": 1,
    "d": 2,
    "e": 2,
    "a": 2,
    "x": 3,
    "r": 3,
    "n": 3,
    "t": 4,
    "ö": 4,
    "w": 5,
    "å": 5,
    "f": 5,
    "h": 5,
    "j": 5,  # Document insight
    # Slash commands (Tier 6)
    "m": 6,  # /recall (memory)
    "k": 6,  # /capture (keep)
    "i": 6,  # /significance (important)
    "b": 6,  # /debug-session (bug)
    "l": 6,  # /ui-prototype (layout)
    "o": 6,  # /consensus-consult (opinions)
    "q": 6,  # /docs-review (quality)
}

# Visual style reference images (for AI prompt context)
STYLE_REFERENCES = [
    "/Users/fredrikbranstrom/Design/kimonokittens-arts-crafts.png",
    "/Users/fredrikbranstrom/Design/kimonokittens-game-night.png",
    "/Users/fredrikbranstrom/Design/kimonokittens-horror-night.png",
    "/Users/fredrikbranstrom/Design/dreams-come-true.jpg",
]


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

        shortcuts.append(
            {
                "key": svorak_key,
                "output": output_text.strip(),
                "tier": tier,
                "tier_name": KEYBOARD_TIER_NAMES.get(tier, f"Tier {tier}"),
            }
        )

    return sorted(shortcuts, key=lambda x: (x["tier"], x["key"]))


def extract_xbox_mappings(config_path: Path) -> list[dict]:
    """Extract Xbox controller mappings from Karabiner config."""
    with open(config_path) as f:
        config = json.load(f)

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

    mappings = []

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

        # Extract output text or key action
        to_action = manipulator["to"][0]
        if "shell_command" in to_action:
            shell_cmd = to_action["shell_command"]
            text_match = re.search(
                r'set the clipboard to [\\"]+"?(.+?)[\\"]+"?\s*\'', shell_cmd
            )
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
        else:
            output = desc

        button_info = BUTTON_LABELS.get(button, (button, None))
        button_name = button_info[0]
        label = button_info[1]

        # Categorize
        if label:
            category = "labeled"
        elif button in ["dpad_left", "dpad_right", "button13"]:
            category = "utility"
        else:
            category = "workflow"

        mappings.append({
            "button": button_name,
            "label": label,
            "output": output,
            "category": category,
            "category_name": XBOX_CATEGORIES[category],
        })

    # Sort: labeled first, then workflow, then utility
    category_order = {"labeled": 0, "workflow": 1, "utility": 2}
    return sorted(mappings, key=lambda x: (category_order[x["category"]], x["button"]))


def build_prompt(keyboard_shortcuts: list[dict], xbox_mappings: list[dict]) -> str:
    """Build the prompt for Nano Banana Pro."""

    # Group keyboard shortcuts by tier
    tiers = {}
    for s in keyboard_shortcuts:
        tier = s["tier"]
        if tier not in tiers:
            tiers[tier] = {"name": s["tier_name"], "shortcuts": []}
        tiers[tier]["shortcuts"].append(s)

    # Build keyboard content - just key → output, no "Caps+" prefix on each line
    keyboard_lines = ["KEYBOARD SHORTCUTS (all use Caps Lock + key):"]
    for tier_num in sorted(tiers.keys()):
        tier = tiers[tier_num]
        keyboard_lines.append(f"\n  {tier['name']}:")
        for s in tier["shortcuts"]:
            # Allow longer text - prioritize showing full content
            output = s["output"][:60] + "..." if len(s["output"]) > 60 else s["output"]
            keyboard_lines.append(f"    {s['key']} → {output}")

    # Group Xbox mappings by category
    xbox_cats = {}
    for m in xbox_mappings:
        cat = m["category"]
        if cat not in xbox_cats:
            xbox_cats[cat] = {"name": m["category_name"], "mappings": []}
        xbox_cats[cat]["mappings"].append(m)

    # Build Xbox content
    xbox_lines = ["\nXBOX CONTROLLER:"]
    category_order = ["labeled", "workflow", "utility"]
    for cat in category_order:
        if cat in xbox_cats:
            xbox_lines.append(f"\n  {xbox_cats[cat]['name']}:")
            for m in xbox_cats[cat]["mappings"]:
                btn = m["button"]
                label = f" ({m['label']})" if m["label"] else ""
                # Allow longer text - prioritize showing full content
                output = m["output"][:55] + "..." if len(m["output"]) > 55 else m["output"]
                xbox_lines.append(f"    {btn}{label} → {output}")

    keyboard_content = "\n".join(keyboard_lines)
    xbox_content = "\n".join(xbox_lines)

    prompt = f"""Create a MINIMAL, REFINED synthwave-style infographic for workflow shortcuts.

NO TITLE - maximize space for content.

TWO SECTIONS - LEFT AND RIGHT:

LEFT COLUMN - KEYBOARD SHORTCUTS:
{keyboard_content}

IMPORTANT FOR KEYBOARD SECTION:
- State "Caps +" ONCE as a header/legend (e.g., "KEYBOARD (Caps + key)")
- DO NOT repeat "Caps Lock" on each individual shortcut badge - wasteful!
- Each shortcut should show just the key letter in a small badge, then the output text
- Example: [u] → Ultrathink   (NOT [Caps Lock] [u] → Ultrathink)

RIGHT COLUMN - XBOX CONTROLLER:
{xbox_content}

CRITICAL FOR XBOX SECTION:
- MUST include a visual diagram/illustration of an Xbox controller
- Show button positions on the actual controller shape
- This controller diagram is REQUIRED - always include it

DESIGN - INSPIRED BY KIMONO KITTENS DASHBOARD (minimalist synthwave):

EXACT COLORS TO USE:
- Background: Dark navy #1a1a2e
- Card backgrounds: Subtle purple-tinted panels with fine 1px borders
- Keyboard section accent: Coral/orange #ff8c42
- Xbox section accent: Electric blue #00d4ff
- Text: Clean white #eaeaea for content, muted #a0a0a0 for labels

TYPOGRAPHY:
- Section headers: Stylized scratchy/distressed synthwave font
- Keys/buttons: Clean monospace in SMALL rounded badges with fine borders
- Output text: Regular sans-serif, readable size
- ALL TEXT MUST BE PERFECTLY LEGIBLE AND CORRECTLY SPELLED

LAYOUT:
- Two-column layout: Keyboard (left), Xbox (right)
- Clean card-based layout with subtle transparency
- Fine lines, NOT thick neon borders
- Subtle gradients, NOT intense glow effects
- Group related items in subsections

VISUAL REAL ESTATE PRIORITY:
- Use saved space to show MORE of the shortcut output text
- Minimize truncation - show as much of each phrase as possible
- Compact key badges, generous space for output text
- The user needs to see what each shortcut types BEFORE pressing it

VISUAL ELEMENTS:
- NO sun/horizon motif, NO chrome effects, NO dripping/glitch effects
- Subtle purple gradient swoosh in background
- Fine hairline borders on cards
- Small keyboard icon for left section header
- Xbox controller diagram for right section (REQUIRED)

Resolution: 2K quality
Aspect ratio: 16:10 (landscape to fit both columns)

CRITICAL - NO WHITE BORDERS:
- The image must have NO white margins, borders, or padding around the edges
- The dark navy background (#1a1a2e) must extend to ALL edges of the image
- Content should go edge-to-edge (with reasonable internal padding)

Think: Modern dashboard UI meets subtle synthwave aesthetic. Clean, functional, beautiful.
CRITICAL: Every single shortcut must be readable. Prioritize legibility and content over decoration."""

    return prompt


def generate_infographic(prompt: str, output_path: Path) -> bool:
    """Generate the infographic using Nano Banana Pro."""

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        return False

    print("Connecting to Gemini API...")
    client = genai.Client(api_key=api_key)

    print("Generating infographic with Nano Banana Pro...")
    print("(This may take 30-60 seconds)")

    try:
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

        # If no image found, check for text response
        for part in response.candidates[0].content.parts:
            if hasattr(part, "text") and part.text:
                print(f"Model response: {part.text[:500]}...")

        print("Error: No image was generated in the response")
        return False

    except Exception as e:
        print(f"Error generating image: {e}")
        return False


def main():
    print("=" * 60)
    print("Karabiner Cheatsheet Generator (Nano Banana Pro)")
    print("=" * 60)

    # Extract keyboard shortcuts
    print(f"\nReading keyboard config: {KEYBOARD_CONFIG_PATH}")
    keyboard_shortcuts = extract_keyboard_shortcuts(KEYBOARD_CONFIG_PATH)
    print(f"Found {len(keyboard_shortcuts)} keyboard shortcuts across {len(KEYBOARD_TIER_NAMES)} tiers")

    # Extract Xbox mappings
    print(f"Reading Xbox config: {XBOX_CONFIG_PATH}")
    xbox_mappings = extract_xbox_mappings(XBOX_CONFIG_PATH)
    print(f"Found {len(xbox_mappings)} Xbox controller mappings")

    # Build combined prompt
    prompt = build_prompt(keyboard_shortcuts, xbox_mappings)
    print(f"\nPrompt length: {len(prompt)} chars")

    success = generate_infographic(prompt, OUTPUT_PNG)

    if success:
        print("\nDone! Open the image with:")
        print(f"  open {OUTPUT_PNG}")
    else:
        print("\nFailed to generate infographic.")
        print("Check GEMINI_API_KEY and try again.")


if __name__ == "__main__":
    main()
