# eMarkaz Course Library — Folder Creation and New File Upload Workflow

## Purpose

This guide explains how to add new folders and upload new books/files to the eMarkaz Course Library website.

Website:

```text
https://emarkazlibrary.com
```

Repository folder:

```text
/c/Linux/emarkaz-course-library
```

---

# 1. Main Folder Structure

Your project now supports these main areas:

```text
emarkaz-course-library/
├── books/
├── emarkaz-books/
├── quran-juzz/
├── generate_file_pages.py
├── index.html
└── CNAME
```

---

# 2. What Each Folder Is For

## `books/`

Use this for course-wise and semester-wise books.

Example:

```text
books/ac-alim-course/semester-01/
books/ac-alim-course/semester-09/
books/dc-ilm-e-deen-course/semester-06/
```

---

## `emarkaz-books/`

Use this for general-purpose eMarkaz books.

Example:

```text
emarkaz-books/e-courses/fiqh/
emarkaz-books/e-courses/grammar/nawh/
emarkaz-books/e-courses/personalities/Scholars/
```

---

## `quran-juzz/`

Use this for Quran Juzz files.

Example:

```text
quran-juzz/
```

You can also create nested folders later:

```text
quran-juzz/para-01/
quran-juzz/para-02/
quran-juzz/translation/
quran-juzz/tafseer/
```

---

# 3. Supported File Types

The generator supports these file types:

```text
.pdf
.docx
.md
.xlsx
.xls
```

Recommended file type for books:

```text
.pdf
```

---

# 4. Important File Size Rule

GitHub has a hard file size limit.

```text
0–50 MB      Best
50–100 MB    Works, but GitHub may show a warning
100+ MB      Push will fail
```

Check for large files before pushing:

```bash
find . -type f -size +95M -print
```

If a file is over 100 MB, do not push it to GitHub.

---

# 5. Go to Repository

Always start here:

```bash
cd /c/Linux/emarkaz-course-library
```

---

# 6. Add New Semester Folder

Example: add AC Semester 11 and 12.

```bash
cd /c/Linux/emarkaz-course-library

mkdir -p books/ac-alim-course/semester-11
mkdir -p books/ac-alim-course/semester-12
```

Because Git does not track empty folders, add `.gitkeep`:

```bash
find books -type d -empty -exec touch {}/.gitkeep \;
```

Then run generator:

```bash
python generate_file_pages.py
```

Then push:

```bash
git status
git add -A
git commit -m "Add new semester folders"
git push origin main
```

---

# 7. Add Nested Folder Inside a Semester

Example: add `Exam Papers` inside AC Semester 08.

```bash
cd /c/Linux/emarkaz-course-library

mkdir -p "books/ac-alim-course/semester-08/Exam Papers"
```

Add `.gitkeep` if empty:

```bash
find books -type d -empty -exec touch {}/.gitkeep \;
```

Run generator:

```bash
python generate_file_pages.py
```

Push:

```bash
git status
git add -A
git commit -m "Add exam papers folder"
git push origin main
```

The generator will create:

```text
books/ac-alim-course/semester-08/index.html
books/ac-alim-course/semester-08/Exam Papers/index.html
```

---

# 8. Add New General Folder Under `emarkaz-books/`

Example: add a new folder called `seerah`.

```bash
cd /c/Linux/emarkaz-course-library

mkdir -p emarkaz-books/e-courses/seerah
```

Add `.gitkeep` if empty:

```bash
find emarkaz-books -type d -empty -exec touch {}/.gitkeep \;
```

Run generator:

```bash
python generate_file_pages.py
```

Push:

```bash
git status
git add -A
git commit -m "Add seerah folder"
git push origin main
```

---

# 9. Add Nested Folder Under `emarkaz-books/`

Example:

```bash
cd /c/Linux/emarkaz-course-library

mkdir -p emarkaz-books/e-courses/fiqh/prayer
mkdir -p emarkaz-books/e-courses/fiqh/fasting
mkdir -p emarkaz-books/e-courses/fiqh/zakat
```

Add `.gitkeep`:

```bash
find emarkaz-books -type d -empty -exec touch {}/.gitkeep \;
```

Run generator:

```bash
python generate_file_pages.py
```

Push:

```bash
git status
git add -A
git commit -m "Add nested fiqh folders"
git push origin main
```

---

# 10. Add New Folder Under `quran-juzz/`

Example:

```bash
cd /c/Linux/emarkaz-course-library

mkdir -p quran-juzz/para-01
mkdir -p quran-juzz/para-02
mkdir -p quran-juzz/para-03
```

Add `.gitkeep`:

```bash
find quran-juzz -type d -empty -exec touch {}/.gitkeep \;
```

Run generator:

```bash
python generate_file_pages.py
```

Push:

```bash
git status
git add -A
git commit -m "Add Quran Juzz folders"
git push origin main
```

---

# 11. Add New PDF Book to Course Semester

Example: add a PDF to AC Semester 09.

First copy your file into the folder.

Example if file is in Downloads:

```bash
cd /c/Linux/emarkaz-course-library

cp "/c/Users/krmar/Downloads/my-book.pdf" "books/ac-alim-course/semester-09/"
```

Then run generator:

```bash
python generate_file_pages.py
```

Push:

```bash
git status
git add -A
git commit -m "Add AC semester 09 book"
git push origin main
```

---

# 12. Add New PDF Book to Nested Semester Folder

Example: add an exam paper PDF.

```bash
cd /c/Linux/emarkaz-course-library

cp "/c/Users/krmar/Downloads/exam-paper.pdf" "books/ac-alim-course/semester-08/Exam Papers/"
```

Run generator:

```bash
python generate_file_pages.py
```

Push:

```bash
git status
git add -A
git commit -m "Add AC semester 08 exam paper"
git push origin main
```

---

# 13. Add New PDF Book to `emarkaz-books/`

Example: add a fiqh book.

```bash
cd /c/Linux/emarkaz-course-library

cp "/c/Users/krmar/Downloads/fiqh-book.pdf" "emarkaz-books/e-courses/fiqh/"
```

Run generator:

```bash
python generate_file_pages.py
```

Push:

```bash
git status
git add -A
git commit -m "Add fiqh book"
git push origin main
```

---

# 14. Add New Quran Juzz File

Example:

```bash
cd /c/Linux/emarkaz-course-library

cp "/c/Users/krmar/Downloads/para-01.pdf" "quran-juzz/"
```

Run generator:

```bash
python generate_file_pages.py
```

Push:

```bash
git status
git add -A
git commit -m "Add Quran Juzz file"
git push origin main
```

---

# 15. If File Name Has Spaces

Use quotes.

Correct:

```bash
cp "/c/Users/krmar/Downloads/My Book Name.pdf" "emarkaz-books/e-courses/fiqh/"
```

Wrong:

```bash
cp /c/Users/krmar/Downloads/My Book Name.pdf emarkaz-books/e-courses/fiqh/
```

---

# 16. If Folder Name Has Spaces

Use quotes.

Example:

```bash
mkdir -p "books/ac-alim-course/semester-08/Exam Papers"
```

Copy file:

```bash
cp "/c/Users/krmar/Downloads/exam paper.pdf" "books/ac-alim-course/semester-08/Exam Papers/"
```

---

# 17. Full Workflow: Add Folder Only

Use this when you create a folder but do not add files yet.

```bash
cd /c/Linux/emarkaz-course-library

mkdir -p emarkaz-books/e-courses/new-folder-name

find emarkaz-books quran-juzz books -type d -empty -exec touch {}/.gitkeep \;

python generate_file_pages.py

git status
git add -A
git commit -m "Add new library folder"
git push origin main
```

---

# 18. Full Workflow: Add New Books/Files

Use this when you add new PDFs, DOCX, MD, or Excel files.

```bash
cd /c/Linux/emarkaz-course-library

# Copy your files into the correct folder first
# Example:
cp "/c/Users/krmar/Downloads/my-book.pdf" "emarkaz-books/e-courses/fiqh/"

python generate_file_pages.py

git status
git add -A
git commit -m "Add new books and update pages"
git push origin main
```

---

# 19. What `generate_file_pages.py` Does

The generator automatically creates `index.html` pages.

It supports:

```text
books/<course>/semester-XX/
books/<course>/semester-XX/nested-folder/

emarkaz-books/
emarkaz-books/any/nested/folder/

quran-juzz/
quran-juzz/any/nested/folder/
```

Example generated pages:

```text
books/ac-alim-course/semester-09/index.html
books/ac-alim-course/semester-08/Exam Papers/index.html

emarkaz-books/index.html
emarkaz-books/e-courses/index.html
emarkaz-books/e-courses/fiqh/index.html

quran-juzz/index.html
```

---

# 20. When to Update Homepage `index.html`

You do **not** need to update homepage for every book.

You only update homepage when you add a new main visible section or want a new button on the homepage.

Examples:

```text
Adding PDF book → no homepage update needed
Adding folder inside emarkaz-books → no homepage update needed
Adding folder inside quran-juzz → no homepage update needed
Adding new semester that should show on homepage → update index.html semester links
Adding brand-new main category → update index.html
```

---

# 21. Add New Semester Link to Homepage

If you add a new semester and want it visible on homepage, add a link like this in `index.html`:

```html
<a class="semester" href="books/ac-alim-course/semester-11/">Semester 11</a>
```

Then run:

```bash
git status
git add -A
git commit -m "Add semester link to homepage"
git push origin main
```

---

# 22. After Push

After pushing, wait for GitHub Pages/GitHub Actions to update.

Then check:

```text
https://emarkazlibrary.com
```

Example pages:

```text
https://emarkazlibrary.com/emarkaz-books/
https://emarkazlibrary.com/quran-juzz/
https://emarkazlibrary.com/books/ac-alim-course/semester-09/
```

---

# 23. Common Errors and Fixes

## Error: empty folder not showing in GitHub

Reason:

```text
Git does not track empty folders.
```

Fix:

```bash
find emarkaz-books quran-juzz books -type d -empty -exec touch {}/.gitkeep \;
```

---

## Error: PDF opens as failed document

Possible reason:

```text
PDF may be stored with Git LFS.
```

Fix:

```bash
git lfs untrack "*.pdf"
git rm --cached -r books emarkaz-books quran-juzz
git add .gitattributes
git add books emarkaz-books quran-juzz
git commit -m "Serve PDFs directly without Git LFS"
git push origin main
```

---

## Error: push fails because file is over 100 MB

Check large files:

```bash
find . -type f -size +95M -print
```

Move large file out of repo:

```bash
mkdir -p /c/Linux/emarkaz-large-files-backup
mv "path/to/large-file.pdf" /c/Linux/emarkaz-large-files-backup/
```

Then regenerate and push:

```bash
python generate_file_pages.py
git add -A
git commit -m "Remove oversized file and update pages"
git push origin main
```

---

# 24. Best Daily Memory Line

```text
Add folder/file → add .gitkeep if folder is empty → run generator → git add/commit/push → check website
```

---

# 25. Best Command Set to Remember

```bash
cd /c/Linux/emarkaz-course-library

find emarkaz-books quran-juzz books -type d -empty -exec touch {}/.gitkeep \;

python generate_file_pages.py

git status
git add -A
git commit -m "Add new books and update pages"
git push origin main
```

Alhamdulillah, this is the clean workflow for maintaining the eMarkaz Course Library.
