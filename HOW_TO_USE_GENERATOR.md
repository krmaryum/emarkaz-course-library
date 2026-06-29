# eMarkaz Course Library Auto Page Generator

This guide explains how to automatically create `index.html` pages for semester folders.

## Supported file types

The script supports:

```text
.pdf
.docx
.md
.xlsx
```

Small correction: Excel files should be `.xlsx`, not `.xlxs`.

## Where to place the script

Put this file in the root of your repo:

```text
/c/Linux/emarkaz-course-library/generate_file_pages.py
```

Your repo should look like:

```text
emarkaz-course-library/
├── index.html
├── README.md
├── generate_file_pages.py
└── books/
    ├── ac-alim-course/
    │   └── semester-01/
    └── dc-ilm-e-deen-course/
```

## How to use

After adding files into any semester folder, run:

```bash
cd /c/Linux/emarkaz-course-library
python generate_file_pages.py
```

The script will automatically create or update `index.html` files inside semester folders.

Example:

```text
books/ac-alim-course/semester-01/index.html
books/ac-alim-course/semester-02/index.html
books/dc-ilm-e-deen-course/semester-01/index.html
```

## Git commands after running the script

```bash
git status
git add -A
git commit -m "Auto-generate course file pages"
git push origin main
```

## Important notes

- Do not use Git LFS for PDFs if you want GitHub Pages to open them in the browser.
- GitHub does not track empty folders. Use `.gitkeep` inside empty folders.
- PDF files can open in the browser.
- DOCX and XLSX files usually download.
- Markdown files can open in the browser as text, or later you can create a special Markdown viewer.

## Recommended file naming

English-safe filenames are best for URLs:

```text
book-01-usool-aqaid.pdf
semester-01-syllabus.docx
schedule.xlsx
```

You can still show Urdu titles on the website, but the script uses the filename as the card title.
