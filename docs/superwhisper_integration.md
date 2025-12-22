# SuperWhisper Integration Reference

> **Purpose**: Complete reference for SuperWhisper configuration, vocabulary management, and integration with Karabiner keyboard/controller shortcuts.
>
> **Last Updated**: December 21, 2025

## File Locations

### Configuration Files

| File | Purpose |
|------|---------|
| `~/Documents/superwhisper/settings/settings.json` | **Main config**: vocabulary, replacements, mode list |
| `~/Documents/superwhisper/modes/*.json` | Per-mode settings (language, voice model, app activation) |
| `~/Library/Preferences/com.superduper.superwhisper.plist` | System preferences (hotkeys as Carbon key codes) |
| `~/Library/Application Support/superwhisper/database/superwhisper.sqlite` | Transcription history database |
| `~/Documents/superwhisper/recordings/` | Audio recording files |

### Reading the Plist (Hotkey Config)

```bash
plutil -p ~/Library/Preferences/com.superduper.superwhisper.plist | grep -i shortcut
```

**Key format**: `{"carbonKeyCode": N, "carbonModifiers": M, "mouseButtonNumbers": []}`

**Carbon key code reference** (ISO Swedish keyboard):
- `50` = Key above Tab (§ on ISO = `non_us_backslash` in Karabiner)
- `53` = Escape
- `40` = K key (used with modifiers)

## Vocabulary vs Replacements

### Vocabulary (Pre-Transcription Hints)

**Location**: `settings.json` → `vocabulary` array

**How it works**: Words sent to Whisper AI during transcription to improve recognition accuracy. The model uses these as hints to correctly identify words that might otherwise be misheard.

**Key insight**: Vocabulary and Replacements are **complementary, not redundant**:
- **Vocabulary**: Helps Whisper *recognize* "Ultrathink" as one word during transcription
- **Replacement**: Catches cases where Whisper still transcribes it as "Ultra think" and fixes it

Both working together = belt AND suspenders.

**Best practices**:
- Add any word that gets frequently misheard (even common English words!)
- Proper nouns, brand names, technical terms are obvious candidates
- Common words like "frontend", "backend", "todo" may still need vocabulary help if Whisper mishears them in your accent/context
- Replacements alone won't help if Whisper transcribes something completely different

**Example**:
```json
"vocabulary": [
  "Graphiti",
  "Serena",
  "Ultrathink",
  "Svorak",
  "Karabiner"
]
```

### Replacements (Post-Transcription Substitution)

**Location**: `settings.json` → `replacements` array

**How it works**: Text substitution AFTER transcription completes. 100% reliable since it's string matching.

**Best practices**:
- Preferred for correcting persistent errors
- Great for expanding abbreviations or trigger phrases
- Can include multi-line text (use `\n` for newlines)

**Example**:
```json
"replacements": [
  {
    "id": "UUID-HERE",
    "original": "docs review",
    "with": "/docs-review"
  },
  {
    "id": "UUID-HERE",
    "original": "Ultra think",
    "with": "Ultrathink"
  }
]
```

## Integration with Karabiner Shortcuts

### Overlap Analysis

SuperWhisper vocabulary should **complement** not duplicate keyboard/controller shortcuts.

**Keyboard shortcuts (Caps+key)** handle:
- Quick confirmations: Ultrathink, Yes!, Continue, Proceed
- Workflow phrases: Sit rep, Git state, Doc coherence, Explore, Delegate
- Actions: Fix this, Explain, Summarize, Run tests, Search online

**Xbox controller** handles:
- Same phrases as keyboard (different input method)
- DICT button triggers SuperWhisper itself

**SuperWhisper replacements** handle:
- Slash command triggers via "run" prefix (e.g., "run recall" → `/recall`)
- Common corrections (clod → Claude, graffiti → Graphiti)
- Proper noun corrections (Frederick → Fredrik)

**SuperWhisper vocabulary** should handle:
- Proper nouns that Whisper might mishear
- Technical terms specific to your stack
- Names of people, projects, tools

### "Run" Prefix Pattern

Slash command voice triggers use **"run" prefix** to avoid collision with normal speech:
- ✅ "run consensus" → `/consensus-consult` (intentional command)
- ✅ "How do we reach consensus on this?" (normal speech, unchanged)

**Exception**: Legacy triggers like "Total recap" are specific enough to not need a prefix.

### Current Vocabulary (55 items)

As of December 21, 2025. Located in `~/Documents/superwhisper/settings/settings.json`.

#### People & Projects
```
Fredrik, Sinan, Rasmus, Sam Rosen, Sam Rosen Art,
Kimono Kittens, Borderland, Deliberus, VD Pro
```

#### AI/LLM Ecosystem
```
Claude, Claude Sonnet, Claude Opus, OpenAI, Anthropic, Gemini, o3,
Graphiti, Serena, Pydantic, PydanticAI, Ultrathink
```

#### Document Processing
```
Unstract, LLMWhisperer, LlamaParse
```

#### Dev Tools & Terminology
```
superwhisper, Karabiner, Svorak, MCP, worktree, shims, idempotent,
HammerSpoon, Lua, AutoGen, AgencySwarm, AgentLoom, Mermaid
```

#### Common Terms (added because they were being misheard)
```
todo, frontend, backend, Git, git
```

#### Git Phrases
```
in git status, git status, git commit, git push, git pull
```

#### Files & Config
```
CLAUDE.md, TODO.md, DONE.md, DEVELOPMENT.md, README.md, .env, .gitignore
```

#### Future Additions to Consider
```
GPT-5-nano, FalkorDB, Fish Audio, ElevenLabs, Playwright, Linear,
LaunchAgent, launchctl, Tier 0, Tier 1, Tier 2, slash command
```

### Current Replacements

As of December 21, 2025.

#### Slash Command Triggers (voice → command)

**Legacy triggers** (specific phrases, no prefix needed):
| Say This | Outputs |
|----------|---------|
| `Total recap` | `/total-recap` |
| `Total review` | `/docs-review` |

**"Run" prefix triggers** (verbatim command names, prevents collision with normal speech):
| Say This | Outputs |
|----------|---------|
| `run docs review` | `/docs-review` |
| `run debug session` | `/debug-session` |
| `run significance` | `/significance` |
| `run recall` | `/recall` |
| `run capture` | `/capture` |
| `run consensus consult` | `/consensus-consult` |
| `run ui prototype` | `/ui-prototype` |

#### Common Corrections
| Original | Replacement |
|----------|-------------|
| `Ultra think` | `Ultrathink` |
| `clod` | `Claude` |
| `clod.md` | `CLAUDE.md` |
| `clod code` | `Claude Code` |
| `cloudcode` | `Claude Code` |
| `Cloud Code` | `Claude Code` |
| `graffiti` | `Graphiti` |
| `Frederick` | `Fredrik` |
| `Wattenthal` | `Vattenfall` |
| `Wattenfall` | `Vattenfall` |

#### Expansions
| Original | Replacement |
|----------|-------------|
| `at web` / `atweb` / `at the web` | `@Web` |
| `Just curious` | `Just curious - only assess and diagnose what the truth is - don't make changes until you have my approval` |

## ISO Keyboard Considerations

### The Problem

On Swedish ISO keyboards, the key above Tab sends a different key code than US ANSI keyboards:

| Keyboard | Key Above Tab | Karabiner Code | Carbon Code |
|----------|---------------|----------------|-------------|
| ANSI (US) | ` ~ (backtick) | `grave_accent_and_tilde` | 50 |
| ISO (Swedish) | § (section) | `non_us_backslash` | 50 |

**Carbon key codes are physical**, not logical. Code 50 means "the key above Tab" regardless of what character it produces.

### SuperWhisper Hotkey

SuperWhisper stores hotkeys as Carbon key codes in the plist:
```
"KeyboardShortcuts_toggleRecording" => "{"carbonKeyCode":50,"carbonModifiers":0}"
```

To trigger this from Karabiner on an ISO keyboard:
```json
{
  "key_code": "non_us_backslash"
}
```

**NOT** `grave_accent_and_tilde` (which would send the wrong key on ISO).

## Syncing Across Devices

SuperWhisper supports configuration sync via license:

1. Enable sync in SuperWhisper preferences
2. All devices with same license share:
   - Vocabulary
   - Replacements
   - Mode configurations

**Note**: `~/Documents/superwhisper/` should remain locally accessible (not cloud-only) since SuperWhisper actively uses it during dictation.

## Backup Strategy

### Essential Files to Back Up

```bash
# Main configuration
~/Documents/superwhisper/settings/settings.json

# Custom modes
~/Documents/superwhisper/modes/*.json

# System preferences (hotkeys)
~/Library/Preferences/com.superduper.superwhisper.plist
```

### Quick Backup Command

```bash
mkdir -p ~/backups/superwhisper
cp ~/Documents/superwhisper/settings/settings.json ~/backups/superwhisper/
cp -r ~/Documents/superwhisper/modes/ ~/backups/superwhisper/modes/
cp ~/Library/Preferences/com.superduper.superwhisper.plist ~/backups/superwhisper/
```

## Troubleshooting

### SuperWhisper Not Activating from Controller

1. **Check Karabiner EventViewer** - Does button press register?
2. **Check key code sent** - Should see `non_us_backslash` (ISO) not `grave_accent_and_tilde`
3. **Check for intercepting rules** - Other Karabiner rules might transform the key
4. **Verify SuperWhisper hotkey** - Check plist for `carbonKeyCode: 50`

### Vocabulary Not Helping

- Too many words can confuse the model
- Try using Replacements instead (more reliable)
- Check if word is being transcribed differently (add that variant to Replacements)

### Finding What SuperWhisper Heard

```bash
# Recent transcriptions in database
sqlite3 ~/Library/Application\ Support/superwhisper/database/superwhisper.sqlite \
  "SELECT * FROM recording ORDER BY rowid DESC LIMIT 5;"
```

## Related Documentation

- `docs/xbox_button_reference.md` - Controller button mappings including DICT
- `CLAUDE.md` - Project overview with shortcut tiers
- `docs/cheatsheet_ai.png` - AI-generated visual keyboard shortcut reference
- `~/.claude/CLAUDE.md` - Global Claude Code rules (TTS daemon, contextual intelligence)

## Version History

| Date | Changes |
|------|---------|
| 2025-12-21 | Initial documentation. ISO keyboard fix (`non_us_backslash`). Vocabulary rationalization analysis. Added "run" prefix pattern for slash command voice triggers. |
| 2025-12-22 | Note: SuperWhisper auto-punctuation adds trailing periods to slash commands. No reliable fix found - manual removal required. |
