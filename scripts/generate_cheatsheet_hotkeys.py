#!/usr/bin/env python3
"""Cheatsheet for everything that is not Caps + key or the Xbox pad: the mouse buttons, the
other Karabiner key remaps, and every Hammerspoon hotkey. Writes docs/cheatsheet_hotkeys.png.

Run:  python3 scripts/generate_cheatsheet_hotkeys.py

The page is rendered from HTML with headless Chrome, so every word on it is exact text (an
image model is never asked to draw words: global CLAUDE.md, "An image model draws the scene,
never the words"). The shortcuts are read from the live configs, and each one needs a line in
the tables below: a mapping that appears in a config without one stops the script with an
error, so a new shortcut cannot go undocumented.

Sources: ~/.config/karabiner/karabiner.json (the selected profile: mouse and § rules, simple
remaps, per-device remaps) and the hs.hotkey calls in ~/.hammerspoon/*.lua.
"""
import html
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "cheatsheet_hotkeys.png"
KARABINER = Path.home() / ".config/karabiner/karabiner.json"
HAMMERSPOON = Path.home() / ".hammerspoon"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# What each mapping does, keyed by what the config says. A config entry with no line here is
# an error (see the module docstring).
MOUSE = {
    "button3": ("Middle button", "Next window of this app, across Spaces"),
    "button4": ("Side button, back", "Wrap the selection in <quote> and paste it"),
    "button5": ("Side button, forward", "Wrap the selection in <before>, paste, add \"Proceed.\""),
}
SECTION_KEY = {  # non_us_backslash (§) with a modifier
    "option": ("⌥ §", "Next window of this app, across Spaces"),
    "command": ("⌘ §", "Next window of this app (⌘`)"),
}
SIMPLE = {
    ("right_command", "right_option"): ("Right ⌘", "acts as Right ⌥"),
    ("right_option", "right_command"): ("Right ⌥", "acts as Right ⌘"),
}
DEVICE = {
    "keypad_hyphen": ("Keypad −", "Mission Control"),
    "keypad_plus": ("Keypad +", "Dashboard"),
}
HAMMERSPOON_KEYS = {  # function bound to the key → (section, what it does)
    "narrateSelection": ("Ruby & narration", "Read the selected text aloud"),
    "summarizeAndNarrate": ("Ruby & narration", "Summarise the selection, then read it aloud"),
    "toggleConversationMode": ("Ruby & narration", "Conversation mode on / off"),
    "toggleRubySleepMode": ("Ruby & narration", "Ruby asleep / awake"),
    "M.toggle": ("Screen", "Goodnight: black screen, desk lights off, Ruby asleep (also 🌙 in the menu bar)"),
    'open("next")': ("VLC (spela)", "Next episode"),
    'open("home")': ("VLC (spela)", "spela's home page"),
}
MOD_SYMBOL = {"ctrl": "⌃", "alt": "⌥", "option": "⌥", "cmd": "⌘", "command": "⌘", "shift": "⇧"}
KEY_NAME = {"forwarddelete": "⌦ (fwd delete)", "section_keycode": "§"}


def karabiner_rows():
    profile = next(p for p in json.loads(KARABINER.read_text())["profiles"] if p.get("selected"))
    mouse, keys = [], []
    for rule in profile.get("complex_modifications", {}).get("rules", []):
        if rule.get("enabled") is False:
            continue
        desc = rule.get("description", "")
        if desc.startswith("Caps Lock"):
            keys.append(("Caps tap", "Escape (hold + key: the Caps Lock sheet)"))
            continue
        if desc.startswith("Xbox"):
            continue  # its own sheet
        for m in rule["manipulators"]:
            frm = m["from"]
            if "pointing_button" in frm:
                mouse.append(MOUSE[frm["pointing_button"]])
            elif frm.get("key_code") == "non_us_backslash":
                mod = frm["modifiers"]["mandatory"][0]
                keys.append(SECTION_KEY[mod])
            else:
                raise SystemExit(f"undocumented Karabiner mapping in '{desc}': {frm}")
    for sm in profile.get("simple_modifications", []):
        keys.append(SIMPLE[(sm["from"]["key_code"], sm["to"][0]["key_code"])])
    for dev in profile.get("devices", []):
        for sm in dev.get("simple_modifications", []):
            keys.append(DEVICE[sm["from"]["key_code"]])
    return mouse, keys


BIND = re.compile(r'hs\.hotkey\.(?:bind|new)\(\{([^}]*)\},\s*("?[\w]+"?)\s*,\s*(?:function\(\)\s*)?([\w.]+(?:\("\w+"\))?)')


def hammerspoon_rows():
    sections = {}
    for f in sorted(HAMMERSPOON.glob("*.lua")):
        for line in f.read_text().splitlines():
            code = line.split("--")[0]
            m = BIND.search(code)
            if not m:
                continue
            mods = [x.strip().strip('"') for x in m.group(1).split(",") if x.strip()]
            key = m.group(2).strip('"')
            target = m.group(3)
            if target not in HAMMERSPOON_KEYS:
                raise SystemExit(f"undocumented Hammerspoon hotkey in {f.name}: {line.strip()}")
            section, what = HAMMERSPOON_KEYS[target]
            combo = " ".join(MOD_SYMBOL[x] for x in mods) + (" " if mods else "") + KEY_NAME.get(key, key.upper())
            if section == "VLC (spela)" and not mods:
                combo += "  (near the end)"
            sections.setdefault(section, []).append((combo, what))
    return sections


CSS = """
@font-face { font-family: Sharp; src: local("Sharp Sans Semibold"); }
body { margin: 0; background: #141a2e; color: #e8ecf4; font-family: "Sharp Sans", "Avenir Next", sans-serif;
       width: 1900px; }
.wrap { padding: 48px 56px 56px; }
h1 { text-align: center; font-size: 56px; font-weight: 800; letter-spacing: 1px; margin: 0 0 36px; color: #fff; }
.cols { display: grid; grid-template-columns: 1fr 1fr; column-gap: 64px; }
h2 { color: #ff8a6a; font-size: 30px; font-weight: 600; margin: 26px 0 14px; }
.row { display: grid; grid-template-columns: 270px 36px 1fr; align-items: center; margin: 0 0 12px; font-size: 21px; }
.key { justify-self: start; border: 2px solid #ff7a5c; border-radius: 9px; padding: 4px 12px; color: #fff;
       box-shadow: 0 0 10px rgba(255,110,80,.35); white-space: nowrap; font-size: 20px; }
.arrow { color: #c9cfdb; text-align: center; }
.what { color: #e8ecf4; line-height: 1.3; }
.foot { margin-top: 30px; text-align: center; color: #8a93a8; font-size: 17px; }
"""


def section(title, rows):
    out = [f"<h2>{html.escape(title)}</h2>"]
    for key, what in rows:
        out.append(f'<div class="row"><span class="key">{html.escape(key)}</span>'
                   f'<span class="arrow">→</span><span class="what">{html.escape(what)}</span></div>')
    return "".join(out)


def page():
    mouse, keys = karabiner_rows()
    hs = hammerspoon_rows()
    left = section("Mouse", mouse) + section("Keys (Karabiner)", keys)
    right = "".join(section(t, hs[t]) for t in ("Ruby & narration", "Screen", "VLC (spela)") if t in hs)
    return (f"<!doctype html><meta charset='utf-8'><style>{CSS}</style><body><div class='wrap'>"
            f"<h1>MOUSE &amp; HOTKEYS</h1><div class='cols'><div>{left}</div><div>{right}</div></div>"
            f"<div class='foot'>Caps Lock + key and the Xbox pad have their own sheets · "
            f"generated from karabiner.json and ~/.hammerspoon by scripts/generate_cheatsheet_hotkeys.py</div>"
            f"</div></body>")


def main():
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "sheet.html"
        src.write_text(page(), encoding="utf-8")
        shot = Path(tmp) / "shot.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=2", "--window-size=1900,1400",
                        "--virtual-time-budget=2000", f"--screenshot={shot}", src.as_uri()],
                       check=True, capture_output=True, timeout=60)
        im = Image.open(shot).convert("RGB")
        bg = im.getpixel((5, im.height - 5))
        px = im.load()
        assert px is not None
        bottom = im.height
        for y in range(im.height - 1, 0, -4):
            if any(px[x, y] != bg for x in range(0, im.width, 7)):
                bottom = min(im.height, y + 60)
                break
        tmp_out = Path(tmp) / "out.png"
        im.crop((0, 0, im.width, bottom)).save(tmp_out)
        OUT.write_bytes(tmp_out.read_bytes())  # overwrite in place so Preview reloads it
    print(f"wrote {OUT}")


if __name__ == "__main__":
    sys.exit(main())
