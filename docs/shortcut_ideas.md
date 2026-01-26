# Keyboard Shortcut Ideas

*Research and ideas for future Karabiner shortcuts. Captured January 2026.*

## Selection Wrapper Family (Caps+Number Keys)

Building on the Caps+2 (`<quote>`) and Caps+3 (`<before>`) pattern: copy selection, wrap in semantic XML tags, paste ready for commentary.

| Key | Tag | Use Case |
|-----|-----|----------|
| 1 | `<context>` | Providing background info to AI |
| 2 | `<quote>` | **Implemented** - Quoting AI output for commentary |
| 3 | `<before>` | **Implemented** - Resuming from transcript |
| 4 | *(lines joined)* | **Implemented** - Clean prose paste |
| 5 | *(ELI5)* | **Implemented** - Load-bearing idea extraction |
| 6 | `<code>` or triple backticks | Code references |
| 7 | `<error>` | Pasting error messages |
| 8 | `<output>` | Command/test output |

**Pattern**: All follow `Cmd+C → wrap → Cmd+V` with semantic tags that signal intent to the AI.

## Workflow Enhancers

| Idea | Description | Complexity |
|------|-------------|------------|
| **Paste + prefix** | Copy selection, prepend "Regarding this: " + paste | Low |
| **Paste + instruction** | Wrap selection, add "What's wrong here?" or "Improve this" | Low |
| **Strip formatting** | Copy selection, paste as plain text (remove invisible chars) | Low |
| **Numbered wrap** | Copy selection, wrap each line with line numbers | Medium |

## AI Interaction Patterns

From TextExpander community and AI prompt management tools:

| Idea | Template | Notes |
|------|----------|-------|
| **Role prefix** | "Act as a senior engineer and review: " + selection | Common prompting pattern |
| **Constraint prefix** | "In 3 sentences or less: " + selection | Output length control |
| **Compare template** | "Compare these approaches: " + selection | Decision support |
| **Critique template** | "What could go wrong with: " + selection | Risk analysis |

## Meta/Utility

| Idea | Description | Complexity |
|------|-------------|------------|
| **Timestamp insert** | Insert current ISO timestamp for session notes | Low |
| **File path insert** | Paste current file path from Finder/terminal | Medium |
| **Git branch insert** | Insert current git branch name | Low |

## Research Sources

- Karabiner-Elements community rules gallery
- TextExpander AI prompts management patterns
- Claude Code keyboard shortcuts reference
- Thomas Frank's macro library (Raycast, Keyboard Maestro)

## Implementation Notes

**Shell command pattern** for copy-wrap-paste:
```bash
osascript -e 'tell application "System Events" to keystroke "c" using command down' \
  -e 'delay 0.2' \
  -e 'set clipContent to the clipboard' \
  -e 'set the clipboard to "<TAG>" & return & clipContent & return & "</TAG>" & return & return' \
  -e 'tell application "System Events" to keystroke "v" using command down'
```

**Considerations**:
- 0.2s delay needed for clipboard to update after Cmd+C
- Number keys don't conflict with Svorak layout (numbers are same position)
- Keep tag names short and semantic
- Two newlines after closing tag positions cursor for follow-up text
