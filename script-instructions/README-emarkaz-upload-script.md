# eMarkaz Upload Script README

## File

```text
upload.sh
```

## Purpose

This script uploads new eMarkaz Course Library folders and files to GitHub Pages.

It is used after adding books, PDFs, course files, nested folders, or Quran Juzz files.

---

## Quick Start

Go to the repository:

```bash
cd /c/Linux/emarkaz-course-library
```

Run the script:

```bash
./upload.sh
```

---

## First-Time Setup

Make the script executable:

```bash
chmod +x upload.sh
```

Then run:

```bash
./upload.sh
```

---

## What It Does

The script automatically:

```text
1. Goes to the repo folder
2. Checks for generate_file_pages.py
3. Checks for files larger than 95 MB
4. Adds .gitkeep to empty folders
5. Generates website pages
6. Runs git status
7. Stages changes
8. Asks for commit message
9. Commits changes
10. Pushes to GitHub
```

---

## Supported Folders

```text
books/
emarkaz-books/
quran-juzz/
```

---

## Supported File Types

```text
.pdf
.docx
.md
.xlsx
.xls
```

---

## Normal Workflow

```text
Add folders/files → run ./upload.sh → website updates
```

---

## Example

```bash
cd /c/Linux/emarkaz-course-library

cp "/c/Users/krmar/Downloads/my-book.pdf" "emarkaz-books/e-courses/fiqh/"

./upload.sh
```

---

## Important Notes

Files should be under 100 MB.

Best practice:

```text
Under 50 MB is best
95 MB or more will show a warning
Over 100 MB will fail on GitHub
```

If you add a new semester and want it visible on the homepage, also add its link in `index.html`.

Example:

```html
<a class="semester" href="books/ac-alim-course/semester-11/">Semester 11</a>
```

---

## Website

```text
https://emarkazlibrary.com
```

## Best Command

```bash
cd /c/Linux/emarkaz-course-library
./upload.sh
```
