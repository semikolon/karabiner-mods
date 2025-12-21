# Nano Banana Pro Cheatsheet Generator

Generate beautiful AI-created infographics for keyboard shortcuts using Google's Nano Banana Pro (Gemini 3 Pro Image).

## What is Nano Banana Pro?

Nano Banana Pro is Google's state-of-the-art image generation model, launched November 2025. It excels at:

- **Legible text rendering** - No AI gibberish, words spelled correctly
- **Infographic generation** - Beautiful, structured visual layouts
- **Search grounding** - Can incorporate real-time data
- **High resolution** - Up to 4K output

Model ID: `gemini-3-pro-image-preview`

## Quick Start

```bash
cd ~/Projects/karabiner-mods

# First time: create venv and install dependencies
uv venv && uv pip install google-genai pillow

# Generate the infographic
.venv/bin/python scripts/generate_cheatsheet_ai.py

# View result
open docs/cheatsheet_ai.png
```

## Requirements

- **GEMINI_API_KEY** environment variable (sourced from `.zshrc`)
- Python packages: `google-genai`, `pillow`
- Project venv at `.venv/` (created with `uv venv`)

## Output

| Attribute | Value |
|-----------|-------|
| File | `docs/cheatsheet_ai.png` |
| Dimensions | ~896 × 1200 px |
| Format | PNG, 8-bit RGB |
| Generation time | 30-60 seconds |

## Customizing the Prompt

Edit `scripts/generate_cheatsheet_ai.py` → `build_prompt()` function.

Key prompt elements:
- **TITLE/SUBTITLE** - Header text
- **CONTENT** - Auto-extracted from `keyboard_text_shortcuts.json`
- **DESIGN REQUIREMENTS** - Colors, style, resolution, aspect ratio

### Color Scheme (Current)

| Tier | Color | Hex |
|------|-------|-----|
| Quick Responses | Teal/Green | `#4ecca3` |
| Workflow Patterns | Yellow/Gold | `#ffc93c` |
| Combo Phrases | Coral/Red | `#ff6b6b` |
| Testing & Research | Purple | `#a855f7` |
| Semantic Actions | Sky Blue | `#38bdf8` |
| Background | Deep Blue | `#1a1a2e` |

### Resolution Options

In the prompt, you can request:
- `Resolution: 2K quality` (default)
- `Resolution: 4K quality`
- `Aspect ratio: 3:4` (portrait, current)
- `Aspect ratio: 16:9` (landscape)

## SVG vs AI Comparison

| Aspect | SVG Generator | Nano Banana Pro |
|--------|---------------|-----------------|
| Script | `generate_cheatsheet.py` | `generate_cheatsheet_ai.py` |
| Output | `cheatsheet.svg` + `.png` | `cheatsheet_ai.png` |
| Speed | Instant | 30-60s |
| Consistency | Identical each run | Unique each run |
| Aesthetics | Programmatic | AI-designed |
| Text accuracy | Perfect | Excellent (rare errors) |
| Dependencies | PIL (optional) | google-genai, pillow |
| Cost | Free | Gemini API usage |

## API Configuration

The script uses:
```python
client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
        temperature=0.7,  # Controls variation
    ),
)
```

- **temperature=0.7** - Balanced creativity/consistency
- Lower (0.3) = More predictable layouts
- Higher (0.9) = More creative variation

## Troubleshooting

### "GEMINI_API_KEY not set"
```bash
echo $GEMINI_API_KEY  # Should show your key
# If empty, check ~/.zshrc sources your secrets
```

### "google-genai not installed"
```bash
cd ~/Projects/karabiner-mods
.venv/bin/python -c "from google import genai"  # Test import
uv pip install google-genai  # Reinstall if needed
```

### Poor text rendering
- Simplify the prompt
- Reduce number of shortcuts displayed
- Try lower temperature (0.5)
- Regenerate (results vary)

## References

- [Google AI - Nano Banana Pro](https://blog.google/technology/ai/nano-banana-pro/)
- [Simon Willison - Nano Banana Pro review](https://simonwillison.net/2025/Nov/20/nano-banana-pro/)
- [Gemini API - Image generation docs](https://ai.google.dev/gemini-api/docs/image-generation)
- [Fast Company - Nano Banana Pro infographics](https://www.fastcompany.com/91448567/google-nano-banana-pro-turns-anything-into-beautiful-infographics)
