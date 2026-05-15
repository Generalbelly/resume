---
name: Update Resume Doc
description: Read and update Nobuyoshi Shimmen's English resume Google Doc via gws CLI
---

# Update Resume Doc

## When to Use

Use this skill when the user wants to:
- Read the current content of the English resume Google Doc
- Update, add, or delete bullets in the Google Doc
- Reflect README.md changes into the Google Doc
- Check what's currently written in the Google Doc

## Document IDs

- **English resume (main):** `1lkghEoKXK8vqbNfuEZe2LljkRcltqW6zjfyl_qXkysM`
- **New layout doc (experimental):** `1sJlS_5AzX3_G-2W1ZwoR3r3f28g0MAZx2gbNDldT5PU`

Default target is the main doc unless the user specifies otherwise.

## Read Document Content

```bash
gws docs documents get --params '{"documentId": "DOC_ID"}' 2>/dev/null | python3 -c "
import json, sys
doc = json.load(sys.stdin)

def walk(content):
    for el in content:
        if 'paragraph' in el:
            text = ''.join(r.get('textRun',{}).get('content','') for r in el['paragraph'].get('elements',[]))
            if text.strip():
                print(f\"{el['startIndex']:5}  {text.rstrip()}\")
        elif 'table' in el:
            for row in el['table'].get('tableRows',[]):
                for cell in row.get('tableCells',[]):
                    walk(cell.get('content',[]))

walk(doc['body']['content'])
"
```

This prints each paragraph with its `startIndex` so you can target specific ranges.

## Update Patterns

All updates use `batchUpdate`. Run multiple operations in **reverse index order** within a single batch to avoid index shifting.

### Replace paragraph text (keep paragraph mark)

```bash
gws docs documents batchUpdate \
  --params '{"documentId": "DOC_ID"}' \
  --json '{
    "requests": [
      {"deleteContentRange": {"range": {"startIndex": START, "endIndex": END_MINUS_1}}},
      {"insertText": {"location": {"index": START}, "text": "NEW TEXT"}}
    ]
  }'
```

- `END_MINUS_1` = paragraph `endIndex - 1` (keeps the paragraph mark `\n`)

### Delete entire paragraph

```bash
{"deleteContentRange": {"range": {"startIndex": START, "endIndex": END}}}
```

- Use full `endIndex` to remove the paragraph mark too

### Insert new paragraph

```bash
{"insertText": {"location": {"index": INSERT_AT}, "text": "NEW LINE\n"}}
```

## Workflow

1. **Read** the doc to get current content and indices
2. **Identify** the paragraph(s) to change (by searching for distinctive text)
3. **Plan** changes in reverse index order
4. **Run** batchUpdate with all changes
5. **Verify** by reading the doc again if needed

## Key Notes

- The doc uses a **2-column table** structure: left column = section labels (Summary, Experience, etc.), right column = content
- Always read with `walk()` above before editing — indices shift after every change
- When making multiple changes, either:
  - Do them in one batch (reverse order), or
  - Re-read the doc between each change (safer)
- `gws` outputs keyring warnings to stderr — always use `2>/dev/null`
