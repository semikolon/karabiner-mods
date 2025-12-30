# Gemini Image Generation Prompt Guide

> Best practices for prompting Gemini 3 Pro Image (Nano Banana Pro) for infographics and reference cards.

## Six Essential Prompt Elements (Google's Framework)

According to Google's official guidance, effective image generation prompts should include:

1. **Subject** - Be specific about what appears (e.g., "Xbox wireless controller with labeled button mappings")
2. **Composition** - Frame the layout (e.g., "Top half = diagram, bottom half = tables")
3. **Action** - Describe what's happening or being shown
4. **Location/Setting** - Context for the image
5. **Style** - Define the aesthetic ("minimalist synthwave", "dark theme", specific colors)
6. **Editing Instructions** - For modifications, be direct and specific

## Key Best Practices

### Structure Your Prompts Clearly
- Use clear section headers (SUBJECT, COMPOSITION, STYLE, etc.)
- Separate data from instructions
- List constraints explicitly

### Be Specific About Data
- Provide EXACT data to display, not vague descriptions
- Say "Show ONLY the data listed above" to prevent AI additions
- Specify what NOT to include (e.g., "no [MODIFIER] tags")

### Prevent Duplicates
- Explicitly state "each item appears EXACTLY once"
- AI image models tend to repeat content; be firm about this

### Style Specifications
- Use specific hex color codes (#1a1a2e, #00d4ff)
- Name the aesthetic style ("minimalist synthwave")
- Specify aspect ratio (16:10 landscape)
- State margin/border requirements explicitly

### For Technical Diagrams
- Provide physical layout details (the model may not know specifics)
- Include position references ("RIGHT side", "TOP edge")
- Describe relationships between elements

## Known Limitations

Gemini image generation struggles with:
- **Text rendering accuracy** - May misspell or garble text
- **Consistent styling** - May not maintain style across complex images
- **Precise layouts** - May not follow exact positioning instructions
- **Aspect ratios** - May not maintain specified dimensions

## Example Prompt Structure

```
Create a [TYPE] infographic.

SUBJECT: [Specific description]
COMPOSITION: [Layout description]
STYLE: [Aesthetic keywords, colors]

[SECTION 1 - Physical/Layout Reference]:
- Detail 1
- Detail 2

EXACT DATA TO DISPLAY:

[DATA SECTION]:
- Item 1 → Description
- Item 2 → Description

LAYOUT SPEC:
- Structural requirement 1
- Structural requirement 2

STYLE SPEC ([style name]):
- Color 1: #hex
- Color 2: #hex
- Constraint: NO [unwanted element]

CONSTRAINTS:
- Firm requirement 1
- Firm requirement 2
```

## Iteration Tips

1. **Start simple** - Add complexity gradually
2. **Check for hallucinations** - AI may add elements not in your data
3. **Regenerate if needed** - Results vary; regenerate for better output
4. **Split complex requests** - Two simpler images > one complex image

## Sources

- [Google: Tips for image generation prompting](https://blog.google/products/gemini/image-generation-prompting-tips/)
- [Google AI: Prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
