# Keyboard Text Shortcuts Report

> Generated: December 21, 2025
> Analysis of **1,117 real user messages** from Claude Code sessions (last 3 months)

---

## Executive Summary

**78% of your messages end with "Ultrathink"** - you're already using this constantly! Analysis reveals clear patterns in affirmations, commands, and common phrases that would benefit from keyboard shortcuts.

---

## 1. Implemented Shortcuts

### Tier 1: Daily Drivers (Implemented Dec 21, 2025)

| Shortcut | Output | Svorak Key | QWERTY Physical |
|----------|--------|------------|-----------------|
| **Caps+u** | `Ultrathink` | u | f |
| **Caps+c** | `Continue. Ultrathink` | c | i |
| **Caps+y** | `Yes! Ultrathink` | y | t |
| **Caps+p** | `Proceed. Ultrathink` | p | r |
| **Caps+s** | `Sit rep. Ultrathink` | s | ; |
| **Caps+g** | `What's the git state? Ultrathink` | g | u |

### Tier 2: Workflow Patterns (Implemented Dec 21, 2025)

| Shortcut | Output | Category |
|----------|--------|----------|
| **Caps+d** | `Make sure key docs are up to date and congruent with our progress. Ultrathink` | Documentation |
| **Caps+e** | `Don't make changes. Explore and report back. Ultrathink` | Exploration |
| **Caps+a** | `Put a subagent on researching this thoroughly. Report back with findings. Ultrathink` | Delegation |

**Caps Lock Dual-Purpose**: Tap alone → Escape | Hold + key → Text shortcut

**Technical fix**: Switched from AppleScript `keystroke` to Karabiner's native `text` field to fix spacing issues

---

## 2. High-Value Shortcut Candidates

### Tier 1: Highest Frequency Combos (Exact Matches)

| Phrase | Count | Suggested Shortcut | Svorak Physical Key |
|--------|-------|-------------------|---------------------|
| `Continue. Ultrathink` | 6x | Caps+c | j |
| `Yes! Ultrathink` | 4x | Caps+y | t |
| `Proceed. Ultrathink` | 4x | Caps+p | r |
| `Yes please! Ultrathink` | 2x | Caps+Shift+y | Shift+t |

### Tier 2: Common Starting Words

| Word | Count | Use Case | Suggested Shortcut |
|------|-------|----------|-------------------|
| `Ok` | 67x | Acknowledgment | Caps+o |
| `Hmm` | 42x | Thinking pause | Caps+h |
| `Yes` | 36x | Affirmation | Caps+y |
| `Great` | 28x | Positive feedback | Caps+Shift+g |
| `Perfect` | 27x | Strong approval | Caps+Shift+p |
| `Cool` | 17x | Casual approval | Caps+k |
| `Amazing` | 12x | Enthusiastic approval | Caps+a |

### Tier 3: Command Starters (Imperatives)

| Command | Count | Suggested Shortcut |
|---------|-------|-------------------|
| `Make...` | 15x | Caps+m |
| `Read...` | 15x | Caps+r |
| `Try...` | 13x | Caps+t |
| `Continue...` | 12x | Caps+c |
| `Update...` | 10x | Caps+Shift+u |
| `Search...` | 7x | Caps+s |
| `Push` | 7x | Caps+Shift+p |

### Tier 4: Quick Endings/Suffixes

| Phrase | Count | Suggested Shortcut |
|--------|-------|-------------------|
| `Sit rep` | 3x | Caps+Shift+s |
| `Push` (as command) | 7x | Caps+Shift+p |

---

## 3. Recommended Implementation (Priority Order)

### Phase 1: Immediate High-Value (5 shortcuts)

| # | Shortcut | Output | Rationale |
|---|----------|--------|-----------|
| 1 | **Caps+c** | `Continue. Ultrathink` | 6x exact, combines two common patterns |
| 2 | **Caps+y** | `Yes! Ultrathink` | 4x exact, common affirmation |
| 3 | **Caps+p** | `Proceed. Ultrathink` | 4x exact, approval + thinking |
| 4 | **Caps+o** | `Ok` | 67x starting word |
| 5 | **Caps+g** | `Great!` | 28x starting word |

### Phase 2: Workflow Commands

| # | Shortcut | Output | Rationale |
|---|----------|--------|-----------|
| 6 | **Caps+s** | `Sit rep. Ultrathink` | Status request |
| 7 | **Caps+r** | `Read ` | 15x command starter (leaves cursor ready) |
| 8 | **Caps+t** | `/total-recap` | Slash command integration |
| 9 | **Caps+d** | `/docs-review` | Slash command integration |

### Phase 3: Casual Responses

| # | Shortcut | Output | Rationale |
|---|----------|--------|-----------|
| 10 | **Caps+h** | `Hmm. ` | 42x thinking starter |
| 11 | **Caps+k** | `Cool. ` | 17x casual approval |
| 12 | **Caps+a** | `Amazing! ` | 12x enthusiastic |

---

## 4. Svorak Key Mapping Reference

For Svorak 6 layout, these are the QWERTY physical keys to use in Karabiner:

| Svorak Letter | QWERTY Physical | Shortcut Purpose |
|---------------|-----------------|------------------|
| c | j | Continue |
| y | t | Yes |
| p | r | Proceed |
| o | s | Ok |
| g | u | Great |
| s | o | Sit rep / Search |
| r | p | Read |
| t | k | /total-recap |
| d | e | /docs-review |
| h | d | Hmm |
| k | v | Cool (kool) |
| a | a | Amazing |

---

## 5. Statistical Summary

```
Total sessions analyzed: 179 files
Total JSONL entries: 48,370
Real user messages: 1,117

Top Patterns:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"...Ultrathink" suffix     878x (78.4%)
"Ok..." starter             67x (6.0%)
"Hmm..." starter            42x (3.8%)
"Yes..." starter            36x (3.2%)
"Great..." starter          28x (2.5%)
"Perfect..." starter        27x (2.4%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Exact Repeated Phrases:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"Continue. Ultrathink"       6x
"Yes! Ultrathink"            4x
"Proceed. Ultrathink"        4x
"Yes please! Ultrathink"     2x
"Continue"                   2x
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Command Starters:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Make    15x    Read      15x
Try     13x    Continue  12x
Do      10x    Update    10x
Push     7x    Search     7x
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 6. Notable Insights

1. **You LOVE Ultrathink** - 78% of messages use it. The Caps+u shortcut will save enormous typing.

2. **Affirmation + Ultrathink combos** are your most common exact phrases. Binding these saves two things at once.

3. **"Ok" and "Hmm"** are thinking-out-loud starters - could be useful as quick acknowledgments.

4. **Command starters** (Make, Read, Try) often need context after them - shortcuts could type the word + space.

5. **Slash commands** (`/total-recap`, `/docs-review`) are already mapped to Xbox controller in Zed but would be useful for terminal CC.

---

## 7. Next Steps

1. ~~**Pick 5 shortcuts** from Phase 1 to implement~~ ✅ **Done** (Dec 21, 2025)
2. ~~**Add to JSON** with correct Svorak mappings~~ ✅ **Done**
3. **Test in Ghostty/Zed** to verify they work
4. **Use for a week** and observe which shortcuts get used
5. **Add Tier 2** based on real usage patterns (documentation & context shortcuts)

---

## Appendix: Raw Data Location

- Session files: `~/.claude/projects/*/`
- Analysis script: Can be re-run to update statistics
- Existing mods: `/Users/fredrikbranstrom/Projects/karabiner-mods/mods/`
