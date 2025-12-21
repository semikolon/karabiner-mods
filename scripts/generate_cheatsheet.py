#!/usr/bin/env python3
"""
Generate a visual cheat sheet for Karabiner keyboard shortcuts.
Reads shortcuts from the JSON config and produces a PNG infographic.

Usage:
    python3 scripts/generate_cheatsheet.py

Output:
    docs/cheatsheet.png
"""

import json
import re
from pathlib import Path

# Try to use PIL, fall back to SVG-only if not available
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Note: PIL not installed. Install with: pip install Pillow")
    print("Generating SVG only...")

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_PATH = PROJECT_ROOT / "mods" / "keyboard_text_shortcuts.json"
OUTPUT_DIR = PROJECT_ROOT / "docs"
OUTPUT_PNG = OUTPUT_DIR / "cheatsheet.png"
OUTPUT_SVG = OUTPUT_DIR / "cheatsheet.svg"

# Design constants
COLORS = {
    'bg': '#1a1a2e',
    'card_bg': '#16213e',
    'accent': '#e94560',
    'text': '#eaeaea',
    'text_dim': '#a0a0a0',
    'key_bg': '#0f3460',
    'key_border': '#e94560',
    'tier1': '#4ecca3',
    'tier2': '#ffc93c',
    'tier3': '#ff6b6b',
    'tier4': '#a855f7',
    'tier5': '#38bdf8',
}

TIER_COLORS = {
    1: '#4ecca3',  # Green - Quick responses
    2: '#ffc93c',  # Yellow - Workflow
    3: '#ff6b6b',  # Red - Combos
    4: '#a855f7',  # Purple - Testing/Research
    5: '#38bdf8',  # Blue - Semantic
}

TIER_NAMES = {
    1: 'Quick Responses',
    2: 'Workflow Patterns',
    3: 'Combo Phrases',
    4: 'Testing & Research',
    5: 'Semantic Actions',
}


def extract_shortcuts(config_path: Path) -> list[dict]:
    """Extract shortcut info from Karabiner config."""
    with open(config_path) as f:
        config = json.load(f)

    shortcuts = []
    manipulators = config['rules'][0]['manipulators']

    for m in manipulators:
        if m['type'] != 'basic':
            continue
        desc = m.get('description', '')
        if not desc.startswith('Caps+'):
            continue

        # Parse description: "Caps+u → Ultrathink (Svorak u = QWERTY f)"
        match = re.match(r'Caps\+(\S+)\s*→\s*(.+?)\s*\(Svorak \S+ = QWERTY (\S+)\)', desc)
        if not match:
            # Try simpler format
            match = re.match(r'Caps\+(\S+)\s*→\s*(.+)', desc)
            if match:
                svorak_key = match.group(1)
                name = match.group(2)
                qwerty_key = m['from']['key_code']
            else:
                continue
        else:
            svorak_key = match.group(1)
            name = match.group(2)
            qwerty_key = match.group(3)

        # Extract the actual text from shell command
        shell_cmd = m['to'][0].get('shell_command', '')
        text_match = re.search(r'set the clipboard to [\\"]+"?(.+?)[\\"]+"?\s*\'', shell_cmd)
        if text_match:
            output_text = text_match.group(1).replace('\\"', '"').replace('\\\\', '\\')
        else:
            output_text = name

        shortcuts.append({
            'svorak': svorak_key,
            'qwerty': qwerty_key,
            'name': name,
            'output': output_text.strip(),
        })

    return shortcuts


def assign_tiers(shortcuts: list[dict]) -> list[dict]:
    """Assign tier based on shortcut characteristics."""
    tier_assignments = {
        # Tier 1: Quick responses (short, simple)
        'u': 1, 'c': 1, 'y': 1, 'p': 1, 's': 1, 'g': 1,
        # Tier 2: Workflow patterns
        'd': 2, 'e': 2, 'a': 2,
        # Tier 3: Combo phrases
        'x': 3, 'r': 3, 'n': 3,
        # Tier 4: Testing & Research
        't': 4, 'ö': 4,
        # Tier 5: Semantic actions
        'w': 5, 'å': 5, 'f': 5, 'h': 5,
    }

    for s in shortcuts:
        s['tier'] = tier_assignments.get(s['svorak'], 1)

    return shortcuts


def generate_svg(shortcuts: list[dict], output_path: Path):
    """Generate SVG cheat sheet."""
    # Sort by tier
    shortcuts = sorted(shortcuts, key=lambda x: (x['tier'], x['svorak']))

    # Group by tier
    tiers = {}
    for s in shortcuts:
        tier = s['tier']
        if tier not in tiers:
            tiers[tier] = []
        tiers[tier].append(s)

    # SVG dimensions
    width = 900
    row_height = 45
    tier_header_height = 40
    padding = 20

    # Calculate height
    total_rows = sum(len(items) for items in tiers.values())
    total_tier_headers = len(tiers)
    height = padding * 2 + 80 + (total_rows * row_height) + (total_tier_headers * tier_header_height) + 40

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="{COLORS["bg"]}"/>',

        # Title
        f'<text x="{width//2}" y="45" text-anchor="middle" font-family="SF Pro Display, -apple-system, Arial, sans-serif" font-size="28" font-weight="bold" fill="{COLORS["text"]}">Karabiner Text Shortcuts</text>',
        f'<text x="{width//2}" y="70" text-anchor="middle" font-family="SF Pro Text, -apple-system, Arial, sans-serif" font-size="14" fill="{COLORS["text_dim"]}">Hold Caps Lock + Key (Svorak Layout)</text>',
    ]

    y = 100

    for tier_num in sorted(tiers.keys()):
        tier_shortcuts = tiers[tier_num]
        tier_color = TIER_COLORS.get(tier_num, COLORS['accent'])
        tier_name = TIER_NAMES.get(tier_num, f'Tier {tier_num}')

        # Tier header
        svg_parts.append(f'<rect x="{padding}" y="{y}" width="{width - padding*2}" height="{tier_header_height - 5}" rx="8" fill="{tier_color}20"/>')
        svg_parts.append(f'<text x="{padding + 15}" y="{y + 25}" font-family="SF Pro Text, -apple-system, Arial, sans-serif" font-size="16" font-weight="600" fill="{tier_color}">{tier_name}</text>')
        y += tier_header_height

        for s in tier_shortcuts:
            # Key badge
            svg_parts.append(f'<rect x="{padding + 10}" y="{y + 5}" width="50" height="32" rx="6" fill="{COLORS["key_bg"]}" stroke="{tier_color}" stroke-width="2"/>')
            svg_parts.append(f'<text x="{padding + 35}" y="{y + 27}" text-anchor="middle" font-family="SF Mono, Monaco, monospace" font-size="16" font-weight="bold" fill="{COLORS["text"]}">{s["svorak"]}</text>')

            # Arrow
            svg_parts.append(f'<text x="{padding + 75}" y="{y + 27}" font-family="SF Pro Text, -apple-system, Arial, sans-serif" font-size="16" fill="{COLORS["text_dim"]}">→</text>')

            # Output text (truncate if needed)
            output = s['output']
            if len(output) > 65:
                output = output[:62] + '...'
            svg_parts.append(f'<text x="{padding + 100}" y="{y + 27}" font-family="SF Pro Text, -apple-system, Arial, sans-serif" font-size="14" fill="{COLORS["text"]}">{output}</text>')

            y += row_height

        y += 10  # Gap between tiers

    # Footer
    svg_parts.append(f'<text x="{width//2}" y="{height - 15}" text-anchor="middle" font-family="SF Pro Text, -apple-system, Arial, sans-serif" font-size="11" fill="{COLORS["text_dim"]}">Generated from mods/keyboard_text_shortcuts.json • All shortcuts end with trailing space for composability</text>')

    svg_parts.append('</svg>')

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(svg_parts))

    print(f"Generated: {output_path}")


def generate_png(shortcuts: list[dict], output_path: Path):
    """Generate PNG cheat sheet using PIL."""
    if not HAS_PIL:
        print("Skipping PNG generation (PIL not available)")
        return

    # Sort by tier
    shortcuts = sorted(shortcuts, key=lambda x: (x['tier'], x['svorak']))

    # Group by tier
    tiers = {}
    for s in shortcuts:
        tier = s['tier']
        if tier not in tiers:
            tiers[tier] = []
        tiers[tier].append(s)

    # Dimensions
    width = 900
    row_height = 45
    tier_header_height = 45
    padding = 25

    total_rows = sum(len(items) for items in tiers.values())
    total_tier_headers = len(tiers)
    height = padding * 2 + 90 + (total_rows * row_height) + (total_tier_headers * tier_header_height) + 50

    # Create image
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)

    # Try to load fonts
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 28)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 14)
        header_font = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 16)
        text_font = ImageFont.truetype("/System/Library/Fonts/SFNS.ttf", 14)
        key_font = ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = title_font
        header_font = title_font
        text_font = title_font
        key_font = title_font

    # Title
    draw.text((width//2, 40), "Karabiner Text Shortcuts", font=title_font, fill=COLORS['text'], anchor="mm")
    draw.text((width//2, 70), "Hold Caps Lock + Key (Svorak Layout)", font=subtitle_font, fill=COLORS['text_dim'], anchor="mm")

    y = 100

    for tier_num in sorted(tiers.keys()):
        tier_shortcuts = tiers[tier_num]
        tier_color = TIER_COLORS.get(tier_num, COLORS['accent'])
        tier_name = TIER_NAMES.get(tier_num, f'Tier {tier_num}')

        # Tier header background
        draw.rounded_rectangle(
            [(padding, y), (width - padding, y + tier_header_height - 8)],
            radius=8,
            fill=tier_color + '33'  # Add alpha
        )
        draw.text((padding + 15, y + tier_header_height//2 - 4), tier_name, font=header_font, fill=tier_color)
        y += tier_header_height

        for s in tier_shortcuts:
            # Key badge
            key_x = padding + 10
            draw.rounded_rectangle(
                [(key_x, y + 6), (key_x + 50, y + 38)],
                radius=6,
                fill=COLORS['key_bg'],
                outline=tier_color,
                width=2
            )
            draw.text((key_x + 25, y + 22), s['svorak'], font=key_font, fill=COLORS['text'], anchor="mm")

            # Arrow
            draw.text((padding + 75, y + 22), "→", font=text_font, fill=COLORS['text_dim'], anchor="mm")

            # Output text
            output = s['output']
            if len(output) > 65:
                output = output[:62] + '...'
            draw.text((padding + 100, y + 22), output, font=text_font, fill=COLORS['text'], anchor="lm")

            y += row_height

        y += 10

    # Footer
    draw.text((width//2, height - 20), "Generated from mods/keyboard_text_shortcuts.json", font=subtitle_font, fill=COLORS['text_dim'], anchor="mm")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, 'PNG')
    print(f"Generated: {output_path}")


def main():
    print("Generating keyboard shortcuts cheat sheet...")
    print(f"Reading config: {CONFIG_PATH}")

    shortcuts = extract_shortcuts(CONFIG_PATH)
    shortcuts = assign_tiers(shortcuts)

    print(f"Found {len(shortcuts)} shortcuts")

    # Generate both formats
    generate_svg(shortcuts, OUTPUT_SVG)
    generate_png(shortcuts, OUTPUT_PNG)

    print("Done!")


if __name__ == '__main__':
    main()
