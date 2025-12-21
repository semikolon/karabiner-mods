# Qualitative Analysis: How Fredrik Uses Claude Code

> Based on reading 1,108 user messages across kimonokittens, brf-auto, and dotfiles projects

---

## Executive Summary

Your Claude Code usage reveals a distinctive **strategic orchestration style** - you use Claude not just as a coder, but as a **project manager, researcher, and thinking partner**. You heavily emphasize documentation coherence, exploration before action, and context preservation across sessions.

---

## 1. Core Communication Patterns

### The "Ultrathink" Pattern (78% of messages)
Not just a suffix - it's a **signal for deeper reasoning**. You use it when:
- Decisions have multiple valid approaches
- You want Claude to consider edge cases
- Debugging something non-obvious
- Strategic/architectural questions

### Thinking-Out-Loud Starters
| Phrase | Meaning |
|--------|---------|
| `Hmm` | Processing, uncertain, skeptical |
| `Wait` | Pausing to reconsider, spotted an issue |
| `Ok` | Acknowledged, ready to proceed |
| `Cool` / `Great` / `Amazing` | Approval, momentum |

### Gentle Corrections
You frequently redirect Claude when it misunderstands:
- *"You don't understand..."*
- *"No I just meant..."*
- *"Wait, that's not what I asked"*
- *"Respond only in X sentences"* (constraining verbosity)

---

## 2. Request Categories (by Intent)

### A. Context & Memory (Very Frequent)
**You constantly ask Claude to recall or refresh context:**

| Example | Intent |
|---------|--------|
| *"Refresh my memory - it doesn't auto-self-learn/adjust?"* | Recall previous decisions |
| *"Read up on that. Ultrathink"* | Load context before acting |
| *"What was the plan?"* | Retrieve documented strategy |
| *"Search for recent memories"* | Query Graphiti |
| *"What documents have been touched this session?"* | Track work |

**Shortcut candidates:**
- `Refresh my memory about...`
- `Read up on...`
- `What was the plan for...?`

---

### B. Status Checks (Very Frequent)
**You frequently want situational awareness:**

| Example | Intent |
|---------|--------|
| *"Sit rep"* | Situation report |
| *"What's the git state?"* | Repository status |
| *"What's next according to the plan?"* | Next steps |
| *"Continue. Sit rep. Ultrathink"* | Resume + status |
| *"Sit rep in 1 paragraph please"* | Concise status |

**Shortcut candidates:**
- `Sit rep. Ultrathink`
- `What's the git state? Ultrathink`
- `What's next? Ultrathink`

---

### C. Documentation Coherence (Signature Pattern)
**This is your most distinctive pattern - obsessive about docs staying in sync:**

| Example | Intent |
|---------|--------|
| *"Make sure the plan doc is up to date"* | Sync documentation |
| *"Keep the plan doc congruent with progress"* | Continuous doc updates |
| *"Make sure all key docs are not lying"* | Verify doc accuracy |
| *"Update the master plan!"* | Explicit doc update |
| *"Check todo.md, claude.md, readme.md..."* | Multi-doc coherence |

**Shortcut candidates:**
- `Update the plan doc. Ultrathink`
- `Make sure docs are congruent. Ultrathink`

---

### D. Exploration Before Action (Frequent)
**You prefer understanding before changing:**

| Example | Intent |
|---------|--------|
| *"Don't make changes but explore and report back"* | Read-only research |
| *"Compare and contrast meticulously and deeply"* | Analysis mode |
| *"Think deeply about that first of all"* | Reasoning before implementation |
| *"Put a subagent on researching this"* | Delegated exploration |
| *"Investigate deeply. Ultrathink"* | Deep research mode |

**Shortcut candidates:**
- `Explore but don't change anything. Ultrathink`
- `Research this deeply. Ultrathink`

---

### E. Git Workflow (Frequent)
**Git operations are woven throughout:**

| Example | Intent |
|---------|--------|
| *"Push"* / *"Yes, push. Ultrathink"* | Deploy changes |
| *"Pull from git!"* | Sync from remote |
| *"Commit everything in logical groups"* | Organized commits |
| *"What's the git state?"* | Status check |
| *"Check if its stuff is in master"* | Branch verification |

**Shortcut candidates:**
- `Push! Ultrathink`
- `Commit in logical groups. Ultrathink`

---

### F. Affirmations & Approvals (Frequent)
**Quick responses to Claude's proposals:**

| Example | Intent |
|---------|--------|
| *"Yes! Ultrathink"* | Approve + think |
| *"Proceed. Ultrathink"* | Green light |
| *"Ok do it! Ultrathink"* | Approve action |
| *"Go ahead"* | Permission |
| *"Continue. Ultrathink"* | Resume work |

**Shortcut candidates:**
- `Continue. Ultrathink`
- `Proceed. Ultrathink`
- `Yes! Ultrathink`

---

### G. Debugging & Troubleshooting (Moderate)
**When things go wrong:**

| Example | Intent |
|---------|--------|
| *"Google this please!"* | Web research |
| *"Why isn't this working?"* | Debug request |
| *"Explain what you're doing and why"* | Transparency request |
| *"Why the heck is that gem required?"* | Confusion/frustration |

**Shortcut candidates:**
- `Google this. Ultrathink`
- `Why isn't this working? Ultrathink`

---

### H. Handoff & Delegation (Moderate)
**Preparing context for other agents/sessions:**

| Example | Intent |
|---------|--------|
| *"Gimme a primer prompt to give to a fresh AI agent"* | Context handoff |
| *"Put a subagent on researching this"* | Delegate task |
| *"Include references to all relevant docs"* | Context packaging |

**Shortcut candidates:**
- `Put a subagent on this. Ultrathink`

---

### I. Constraint/Brevity Requests (Moderate)
**You often constrain Claude's verbosity:**

| Example | Intent |
|---------|--------|
| *"Respond only in 2 sentences max"* | Force brevity |
| *"Bullet list of max 10 lines"* | Structured brevity |
| *"Gimme a 3-paragraph summary"* | Controlled length |
| *"In a sentence or two"* | Minimal response |

**Shortcut candidates:**
- `In 2 sentences max. Ultrathink`
- `Brief summary please. Ultrathink`

---

## 3. Recommended Shortcuts (Qualitative Priority)

Based on **intent frequency** and **typing effort saved**:

### Tier 1: Daily Drivers

| Shortcut | Output | Why |
|----------|--------|-----|
| **Caps+c** | `Continue. Ultrathink` | Most common flow continuation |
| **Caps+p** | `Proceed. Ultrathink` | Approval + thinking |
| **Caps+y** | `Yes! Ultrathink` | Quick affirmation |
| **Caps+s** | `Sit rep. Ultrathink` | Status checks |
| **Caps+g** | `What's the git state? Ultrathink` | Git status |

### Tier 2: Documentation & Context

| Shortcut | Output | Why |
|----------|--------|-----|
| **Caps+d** | `Update the plan doc. Ultrathink` | Your signature pattern |
| **Caps+r** | `Read up on ` | Context loading (cursor ready) |
| **Caps+m** | `Refresh my memory about ` | Memory retrieval |

### Tier 3: Research & Exploration

| Shortcut | Output | Why |
|----------|--------|-----|
| **Caps+e** | `Explore but don't make changes. Ultrathink` | Read-only mode |
| **Caps+Shift+g** | `Google this please. Ultrathink` | Web research |
| **Caps+Shift+s** | `Put a subagent on researching this. Ultrathink` | Delegation |

### Tier 4: Brevity Constraints

| Shortcut | Output | Why |
|----------|--------|-----|
| **Caps+b** | `Brief summary please. Ultrathink` | Constrain verbosity |
| **Caps+2** | `In 2 sentences max. ` | Force brevity |

---

## 4. Insights About Your Workflow

1. **You treat Claude as a project manager**, not just a coder. Documentation coherence is paramount.

2. **Exploration before action** is a strong pattern. You rarely say "just do it" - you want understanding first.

3. **Multi-machine orchestration** (Mac + Dell) means you care about context handoffs and session primers.

4. **Bilingual fluency** - you switch between Swedish and English naturally. Shortcuts should probably be English since that's your coding language.

5. **Subagent delegation** is a key tool - you frequently spin off research tasks.

6. **"Ultrathink" is non-negotiable** - it's in 78% of messages. Every shortcut should include it by default.

7. **Git workflow is deeply integrated** - push/pull/commit are conversational, not ceremonial.

---

## 5. Implementation Status

### ✅ Tier 1 Implemented (Dec 21, 2025)

| Shortcut | Output | Status |
|----------|--------|--------|
| **Caps+u** | `Ultrathink` | ✅ Implemented |
| **Caps+c** | `Continue. Ultrathink` | ✅ Implemented |
| **Caps+y** | `Yes! Ultrathink` | ✅ Implemented |
| **Caps+p** | `Proceed. Ultrathink` | ✅ Implemented |
| **Caps+s** | `Sit rep. Ultrathink` | ✅ Implemented |
| **Caps+g** | `What's the git state? Ultrathink` | ✅ Implemented |

### ✅ Tier 2 Implemented (Dec 21, 2025)

Based on qualitative analysis of 1,108 user messages, crafted optimal phrasings for three key workflow patterns:

| Shortcut | Output | Category |
|----------|--------|----------|
| **Caps+d** | `Make sure key docs are up to date and congruent with our progress. Ultrathink` | Documentation Coherence |
| **Caps+e** | `Don't make changes. Explore and report back. Ultrathink` | Exploration Before Action |
| **Caps+a** | `Put a subagent on researching this thoroughly. Report back with findings. Ultrathink` | Delegation |

**Phrase synthesis methodology:**
- Extracted all messages matching each category (527 documentation, 365 exploration, 267 delegation)
- Identified common vocabulary: "congruent", "up to date", "report back", "thoroughly"
- Combined patterns into general-purpose phrases that save maximum typing

### Next Steps

1. **Test in Ghostty/Zed** to verify all shortcuts work correctly
2. **Use for a week** and observe which shortcuts get the most use
3. **Consider context-aware shortcuts** (different outputs in different apps?)
