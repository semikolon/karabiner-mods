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

Search through Claude Code transcript files in `~/.claude/projects/` to extract user messages.

**Data availability note**:
- **JSONL transcripts**: November 26, 2025+ (~191 files)
- **Cache JSON files**: September 2025+ (full history preserved despite v2.0.49 breaking change)
- **History.jsonl**: 5,024 entries, September 2025+

```bash
# PRIMARY: Extract from JSONL transcripts (Nov 26+)
find ~/.claude/projects -name "*.jsonl" -type f -exec grep -h '"type":"user"' {} \; 2>/dev/null | head -5000

# EXTENDED: Extract from cache JSON files (Sept 2025+ - older data!)
find ~/.claude/projects -path "*/cache/*.json" -type f -exec cat {} \; 2>/dev/null | grep -o '"content":"[^"]*"' | head -3000

# HISTORY: Extract from history.jsonl (all prompts, Sept 2025+)
grep -o '"prompt":"[^"]*"' ~/.claude/history.jsonl 2>/dev/null | head -3000

# Count total messages available
find ~/.claude/projects -name "*.jsonl" -type f -exec grep -c '"type":"user"' {} \; 2>/dev/null | awk '{s+=$1} END {print "JSONL user messages:", s}'

# Filter by project if needed
find ~/.claude/projects -path "*dotfiles*" -name "*.jsonl" -exec grep -h '"type":"user"' {} \; 2>/dev/null
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

## Step 7: Xbox Controller Combo Analysis (NEW)

When analyzing for Xbox controller LB+/RB+ modifier combos, consider:

### Semantic Layer Discovery
Don't assume "Research vs Action" division. Let the data reveal natural groupings:
- What verbs/intents cluster together?
- What workflows have clear phases (investigate → decide → execute)?
- What's complementary to existing keyboard shortcuts?

### Existing Coverage Check
Before suggesting new combos, verify they don't duplicate:
- 26 keyboard shortcuts (Caps+key)
- 12 base Xbox buttons (A, B, X, Y, LB, RB, View, Menu, Guide, D-pad, Sticks)

### Couch Mode Considerations
Identify phrases useful when away from keyboard/mouse:
- Navigation commands (spaces, windows, apps)
- Status checks (can trigger without typing follow-up)
- Confirmation/approval (lazy couch agreement)

### Modifier Layer Candidates
For each promising phrase, suggest:
- **LB+ (Layer 1)**: [semantic meaning TBD by data]
- **RB+ (Layer 2)**: [semantic meaning TBD by data]
- **Neither**: Better as keyboard shortcut or base button

### Output Format for Xbox Combos

| Phrase | Layer | Button | Rationale |
|--------|-------|--------|-----------|
| "Analyze this..." | LB+ | A | Investigation intent |
| "Commit and push..." | RB+ | A | Execution intent |

---

**Remember**: All shortcut outputs should end with a trailing space for composability.
