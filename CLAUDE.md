# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bilingual (Japanese/English) resume repository.

- `README.md` — Japanese resume (職務経歴書), manually maintained
- `README.pdf` — Japanese PDF (generated externally, e.g. browser print)
- `en/resume.yaml` — **Single source of truth** for all English resume content
- `en/README.md` — English resume (generated from YAML)
- `en/Resume.pdf` — English PDF (generated from YAML)
- `en/generate.py` — Generator script (reads YAML, outputs both README.md and Resume.pdf)

## Generating English Resume

```bash
python3 en/generate.py
```

This generates both `en/README.md` and `en/Resume.pdf` from `en/resume.yaml`.

Requires Python 3 with `reportlab` and `pyyaml` (`pip3 install reportlab pyyaml`).

## Workflow

**English resume:** Edit `en/resume.yaml`, then run `python3 en/generate.py`. Never edit `en/README.md` directly — it will be overwritten.

**Japanese resume:** Edit `README.md` directly. Keep content in sync with the English YAML manually.

## Commit Messages

Written in Japanese using conventional format: `修正:`, `更新:`, `追加:` prefixes. No co-author attribution (disabled in settings).
