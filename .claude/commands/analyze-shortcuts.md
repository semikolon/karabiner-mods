# Analyze Historical Messages for New Keyboard Shortcuts

You are analyzing the user's Claude Code message history to suggest new keyboard text shortcuts for the karabiner-mods project.

## Context

This project creates Karabiner-Elements shortcuts that type common phrases when holding Caps Lock + a key. The user uses Svorak keyboard layout, so key mappings must account for Svorak→QWERTY translation.

## Step 1: Load Current Shortcuts

Read the current shortcuts from `mods/keyboard_text_shortcuts.json` to understand:
- Which Svorak keys are already mapped
- What phrases are already available
- The pattern/tier structure (Tier 1: quick responses, Tier 2: workflow patterns, Tier 3: combo phrases)

## Step 2: Extract Historical User Messages

Search through Claude Code transcript files in `~/.claude/projects/` to extract user messages. Focus on the last 6-12 months of activity.

```bash
# Extract user messages from JSONL transcripts
find ~/.claude/projects -name "*.jsonl" -mtime -180 -exec grep -h '"type":"user"' {} \; 2>/dev/null | head -2000
```

## Step 3: Pattern Analysis

Analyze the extracted messages for:

### A. Phrase Endings
- Messages ending with "Ultrathink" or similar trigger words
- Common instruction closers

### B. Combo Patterns  
- Multi-part requests using "then", "also", "and then", "after that"
- Chained instructions that could be single shortcuts

### C. High-Value Phrases
- Phrases longer than 5 words (more keystrokes saved)
- Frequently repeated instructions
- Workflow triggers (git, docs, testing, exploration)

### D. Category Analysis
Group findings into categories:
- **Confirmation/Continuation**: "Yes", "Continue", "Proceed"
- **Git Operations**: commit, push, status, diff
- **Documentation**: update docs, check coherence
- **Exploration**: read first, investigate, research
- **Delegation**: subagent, background task
- **Planning**: what's next, priorities, blockers
- **Quality**: review, test, validate

## Step 4: Suggest New Shortcuts

For each promising phrase, provide:
1. **The phrase** (exact wording)
2. **Character count** (value = keystrokes saved)
3. **Frequency** (how often it appears)
4. **Category** (which tier it fits)
5. **Suggested Svorak key** with QWERTY equivalent

### Available Svorak Keys (not yet mapped)
Reference the current shortcuts and identify unmapped keys. Common good choices:
- Home row: prioritize for frequent shortcuts
- Mnemonic: match key to phrase meaning (e.g., 't' for test)

### Svorak → QWERTY Reference
```
Svorak: å ä ö p y f g c r l
QWERTY: q w e r t y u i o p

Svorak: a o e u i d h t n s
QWERTY: a s d f g h j k l ;

Svorak: . q j k x b m w v z
QWERTY: z x c v b n m , . /
```

## Step 5: Present Recommendations

Format your findings as a ranked list:

| Rank | Phrase | Chars | Freq | Category | Svorak Key | QWERTY |
|------|--------|-------|------|----------|------------|--------|
| 1 | "Example phrase here" | 45 | 12 | workflow | t | k |

Include rationale for top 3-5 recommendations.

## Step 6: Implementation Preview

For approved shortcuts, show the JSON snippet that would be added:

```json
{
  "type": "basic",
  "description": "Caps+KEY → PHRASE (Svorak KEY = QWERTY QKEY)",
  "from": { "key_code": "QKEY", "modifiers": { "optional": ["any"] } },
  "to": [{ "shell_command": "osascript ..." }],
  "conditions": [{ "type": "variable_if", "name": "caps_lock_held", "value": 1 }]
}
```

---

**Remember**: All shortcut outputs should end with a trailing space for composability.
