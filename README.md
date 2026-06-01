# Business: Markets & Organizations — Study Materials

Organized lecture notes, a navigable PDF, and an **interactive 100-question practice exam** for the *Markets & Organizations* course.

## Interactive practice exam

**[Take the exam online →](https://T0x1cKos.github.io/business-markets-organizations/)**

- Click answers for instant feedback (correct / incorrect + explanation)
- Live score tracker and filters (unanswered / wrong / correct)
- Works offline — download the HTML or clone this repo

## What's included

| File | Description |
|------|-------------|
| `index.html` | Interactive 100 MCQ practice exam (GitHub Pages) |
| `Business Extra Notes 2 - Organized.pdf` | Full notes with clickable table of contents & bookmarks |
| `Business Extra Notes 2  2 2.pdf` | Original notes (unchanged) |
| `Business - Practice Exam (100 MCQs).pdf` | Printable exam + answer key |

## Regenerate files

```bash
python3 -m venv .venv
.venv/bin/pip install pymupdf
.venv/bin/python build_organized.py   # organized notes PDF
.venv/bin/python build_exam.py        # exam PDF + HTML
cp "Business - Practice Exam (100 MCQs).html" index.html
```
