# eMarkaz Controlled Flexible Generator README

## Purpose

This generator creates clean `index.html` pages for approved public library folders only.

It is more flexible than the old generator because you can add new public root folders later.

It is also safer than scanning the whole repository blindly.

---

## File

```text
generate_file_pages.py
```

---

## Current Public Roots

The generator currently creates pages inside:

```text
books/
emarkaz-books/
quran-juzz/
```

These are controlled in the script:

```python
PUBLIC_LIBRARY_ROOTS = [
    "books",
    "emarkaz-books",
    "quran-juzz",
]
```

---

## Why Not Scan Whole Root Blindly?

Because your repo also has folders like:

```text
.git/
assets/
old/
md/
```

If the generator scans everything, it may create unwanted pages in places that should not be public library sections.

So the better professional design is:

```text
Only generate pages for approved public roots.
```

---

## Add a New Public Root Folder

Example: add a new root folder called:

```text
arabic-books/
```

Step 1: create the folder:

```bash
cd /c/Linux/emarkaz-course-library
mkdir -p arabic-books
```

Step 2: open `generate_file_pages.py` and update:

```python
PUBLIC_LIBRARY_ROOTS = [
    "books",
    "emarkaz-books",
    "quran-juzz",
    "arabic-books",
]
```

Step 3: run upload:

```bash
./upload.sh
```

---

## Normal Workflow

```bash
cd /c/Linux/emarkaz-course-library

# create folders or add files

./upload.sh
```

---

## Supported Files

```text
.pdf
.docx
.md
.xlsx
.xls
.txt
```

---

## What It Generates

Example:

```text
books/index.html
books/ac-alim-course/index.html
books/ac-alim-course/semester-11/index.html

emarkaz-books/index.html
emarkaz-books/e-courses/index.html
emarkaz-books/e-courses/fiqh/index.html

quran-juzz/index.html
quran-juzz/para-01/index.html
```

---

## Relationship With Homepage Helper

The generator creates folder pages.

The homepage helper adds selected folder buttons to the homepage.

They are different jobs:

```text
generate_file_pages.py     creates pages
homepage_link_helper.py    adds homepage buttons when you choose
upload.sh                  runs both and pushes
```

---

## Best Memory Line

```text
Generator creates pages only for approved public roots.
Homepage helper asks before adding homepage links.
```
