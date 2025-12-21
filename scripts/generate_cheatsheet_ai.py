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
CONFIG_PATH = PROJECT_ROOT / "mods" / "keyboard_text_shortcuts.json"
OUTPUT_DIR = PROJECT_ROOT / "docs"
OUTPUT_PNG = OUTPUT_DIR / "cheatsheet_ai.png"

# Tier configuration
TIER_NAMES = {
    1: "Quick Responses",
    2: "Workflow Patterns",
    3: "Combo Phrases",
    4: "Testing & Research",
    5: "Semantic Actions",
    6: "Slash Commands",
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


def extract_shortcuts(config_path: Path) -> list[dict]:
    """Extract shortcut info from Karabiner config."""
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
                "tier_name": TIER_NAMES.get(tier, f"Tier {tier}"),
            }
        )

    return sorted(shortcuts, key=lambda x: (x["tier"], x["key"]))


def build_prompt(shortcuts: list[dict]) -> str:
    """Build the prompt for Nano Banana Pro."""

    # Group by tier
    tiers = {}
    for s in shortcuts:
        tier = s["tier"]
        if tier not in tiers:
            tiers[tier] = {"name": s["tier_name"], "shortcuts": []}
        tiers[tier]["shortcuts"].append(s)

    # Build the content description
    content_lines = []
    for tier_num in sorted(tiers.keys()):
        tier = tiers[tier_num]
        content_lines.append(f"\n{tier['name']}:")
        for s in tier["shortcuts"]:
            # Truncate long outputs for the prompt
            output = s["output"][:50] + "..." if len(s["output"]) > 50 else s["output"]
            content_lines.append(f"  {s['key']} → {output}")

    shortcut_content = "\n".join(content_lines)

    prompt = f"""Create a stunning SYNTHWAVE/RETROWAVE style infographic cheat sheet for keyboard shortcuts.

TITLE: "Karabiner Text Shortcuts"
SUBTITLE: "Hold Caps Lock + Key (Svorak Layout)"

CONTENT TO DISPLAY:
{shortcut_content}

DESIGN REQUIREMENTS - SYNTHWAVE AESTHETIC:
- Dark background with deep purple/magenta gradient (#1a1a2e → #2d1b4e)
- NEON GLOW effects on text and borders - hot pink, electric cyan, sunset orange
- 80s retro-futuristic vibe with chrome/metallic accents
- Sun/horizon motif or grid lines in background (subtle)
- Each tier section with distinct NEON accent color:
  - Quick Responses: Electric Teal (#4ecca3) with glow
  - Workflow Patterns: Neon Gold (#ffc93c) with glow
  - Combo Phrases: Hot Pink/Coral (#ff6b6b) with glow
  - Testing & Research: Neon Purple (#a855f7) with glow
  - Semantic Actions: Electric Cyan (#38bdf8) with glow
  - Slash Commands: Sunset Orange (#ff8c42) with glow
- Keys in glowing rounded badge style with neon borders
- Bold stylized typography - think 80s chrome lettering for title
- Use monospace font for keys, bold sans-serif for descriptions
- Resolution: 2K quality
- Aspect ratio: 3:4 (portrait)
- All text must be perfectly legible and spelled correctly
- Dripping/glitch effects optional on headers

Think: Kimono Kittens band poster meets developer cheat sheet. Outrun aesthetic meets productivity tool.

Make it VISUALLY STRIKING and memorable while keeping all information clearly readable."""

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
    print(f"\nReading config: {CONFIG_PATH}")

    shortcuts = extract_shortcuts(CONFIG_PATH)
    print(f"Found {len(shortcuts)} shortcuts across {len(TIER_NAMES)} tiers")

    prompt = build_prompt(shortcuts)
    print(f"\nPrompt length: {len(prompt)} chars")

    success = generate_infographic(prompt, OUTPUT_PNG)

    if success:
        print("\nDone! Open the image with:")
        print(f"  open {OUTPUT_PNG}")
    else:
        print("\nFailed to generate infographic.")
        print("Falling back to SVG generator...")
        print("  python3 scripts/generate_cheatsheet.py")


if __name__ == "__main__":
    main()
