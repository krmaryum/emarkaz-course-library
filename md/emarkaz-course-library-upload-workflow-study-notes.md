# eMarkaz Course Library — GitHub Pages Upload Workflow Study Notes

## 1. Project Goal

The **eMarkaz Course Library** project is a static website hosted with **GitHub Pages**.

The purpose of the project is to organize religious course materials class-wise, course-wise, and semester-wise.

The website contains course folders and semester folders where students can open or download files such as:

- PDF books
- DOCX documents
- Markdown notes
- Excel XLSX files

---

## 2. Important GitHub Pages Rule

GitHub Pages can serve static files like:

```text
.html
.css
.js
.pdf
.md
.docx
.xlsx
```

But GitHub Pages does **not** automatically list files inside folders like Apache or Nginx.

So if you open a folder URL like:

```text
/books/ac-alim-course/semester-01/
```

GitHub Pages looks for:

```text
/books/ac-alim-course/semester-01/index.html
```

If `index.html` does not exist inside that folder, GitHub Pages shows:

```text
404 File not found
```

---

## 3. Why We Created a Generator Script

Instead of manually writing book cards inside every semester `index.html`, we created a Python script:

```text
generate_file_pages.py
```

This script automatically scans semester folders and creates or updates `index.html` pages.

Supported file types:

```text
.pdf
.docx
.md
.xlsx
```

---

## 4. Recommended Folder Structure

```text
emarkaz-course-library/
│
├── index.html
├── README.md
├── generate_file_pages.py
├── upload.sh
│
├── assets/
│
└── books/
    ├── ac-alim-course/
    │   ├── semester-01/
    │   ├── semester-02/
    │   ├── semester-03/
    │   └── semester-04/
    │
    ├── dc-ilm-e-deen-course/
    │   ├── semester-01/
    │   └── semester-02/
    │
    ├── tif-takhasus-fil-ifta/
    │   ├── semester-01/
    │   └── semester-02/
    │
    └── tfa-takhasus-fil-aqaid/
        ├── semester-01/
        └── semester-02/
```

---

## 5. Four Main Courses

```text
AC  - Alim Course              - عالم کورس
DC  - Ilm-e-Deen Course        - علم دین کورس
TIF - Takhasus fil Ifta        - تخصص فی الافتاء
TFA - Takhasus fil Aqaid       - تخصص فی العقائد
```

---

## 6. Why Empty Folders Disappear on GitHub

Git does **not** track empty folders.

If a folder has no files inside it, GitHub will not show it.

Example:

```text
books/ac-alim-course/semester-05/
```

If this folder is empty, it will vanish from GitHub after push.

To keep an empty folder, add a placeholder file:

```text
.gitkeep
```

Command:

```bash
find books -type d -empty -exec touch {}/.gitkeep \;
```

Then push:

```bash
git add -A
git commit -m "Keep empty folders with gitkeep"
git push origin main
```

---

## 7. Normal Upload Workflow

Use these commands when all files are under 100 MB:

```bash
cd /c/Linux/emarkaz-course-library

python generate_file_pages.py

git status

git add -A

git commit -m "Add semester files and update pages"

git push origin main
```

---

## 8. Why We Use `git add -A`

`git add -A` stages everything:

```text
new files
modified files
deleted files
```

This is important because the project may include:

- New PDF books
- Updated semester `index.html` pages
- Deleted old files
- Removed `.gitkeep` files
- Updated generated pages

Simple meaning:

```text
Git, take my current local project exactly as it is and prepare it for commit.
```

---

## 9. Using the Upload Script

We created an upload script to automate the process:

```text
upload.sh
```

The script does:

1. Goes to the repository folder
2. Runs `generate_file_pages.py`
3. Shows `git status`
4. Runs `git add -A`
5. Asks for a custom commit message
6. Uses a default commit message if Enter is pressed
7. Commits changes
8. Pushes to GitHub

Run the script:

```bash
cd /c/Linux/emarkaz-course-library

chmod +x upload.sh

./upload.sh
```

---

## 10. Upload Script Example

```bash
#!/bin/bash

# ============================================================
# eMarkaz Course Library Upload Script
# ============================================================
# Description:
# This script automates the upload workflow for the eMarkaz
# Course Library project.
#
# What it does:
# 1. Goes to the eMarkaz course library repository.
# 2. Runs generate_file_pages.py to automatically create/update
#    semester index.html pages for supported files.
# 3. Shows Git status.
# 4. Stages all changes using git add -A.
# 5. Asks the user for a custom commit message.
# 6. If the user presses Enter without typing anything, it uses
#    the default commit message.
# 7. Commits and pushes changes to GitHub main branch.
#
# Supported file types depend on generate_file_pages.py:
# .pdf, .docx, .md, .xlsx
# ============================================================

set -e

REPO_DIR="/c/Linux/emarkaz-course-library"
DEFAULT_COMMIT_MESSAGE="Add semester files and update pages"

echo "=========================================="
echo " eMarkaz Course Library Upload Script"
echo "=========================================="
echo
echo "Description:"
echo "This script generates course pages, stages changes,"
echo "commits them, and pushes them to GitHub."
echo

cd "$REPO_DIR" || {
  echo "ERROR: Repository folder not found: $REPO_DIR"
  exit 1
}

echo "Current folder:"
pwd
echo

echo "Step 1: Generating course pages..."
python generate_file_pages.py
echo

echo "Step 2: Checking Git status..."
git status
echo

echo "Step 3: Staging all changes..."
git add -A
echo

if git diff --cached --quiet; then
  echo "No changes to commit."
  echo "Nothing was pushed."
  exit 0
fi

echo "Step 4: Commit message"
echo "Default commit message:"
echo "$DEFAULT_COMMIT_MESSAGE"
echo
read -p "Enter custom commit message, or press Enter to use default: " USER_COMMIT_MESSAGE

if [ -z "$USER_COMMIT_MESSAGE" ]; then
  COMMIT_MESSAGE="$DEFAULT_COMMIT_MESSAGE"
else
  COMMIT_MESSAGE="$USER_COMMIT_MESSAGE"
fi

echo
echo "Using commit message:"
echo "$COMMIT_MESSAGE"
echo

echo "Step 5: Committing changes..."
git commit -m "$COMMIT_MESSAGE"
echo

echo "Step 6: Pushing to GitHub..."
git push origin main
echo

echo "Done. Your GitHub Pages website will update shortly."
```

---

## 11. GitHub File Size Limit

GitHub blocks files larger than:

```text
100 MB
```

Example error:

```text
File is 109.07 MB; this exceeds GitHub's file size limit of 100.00 MB
GH001: Large files detected
```

---

## 12. Check Large Files Before Push

Before pushing, check files bigger than around 95 MB:

```bash
find books -type f -size +95M -print
```

If this command prints a file, that file may be too large for GitHub.

---

## 13. If a File Is Bigger Than 100 MB

Options:

```text
1. Compress the PDF below 100 MB
2. Split the PDF into parts
3. Host the large file somewhere else, like Google Drive
4. Move the file outside the repo
```

Move large file outside repo:

```bash
mkdir -p /c/Linux/emarkaz-large-files-backup

mv "books/ac-alim-course/semester-05/MusnadUlImamIlAazamAlBushraColor مسند الإمام الأعظم ابي حنيفة.pdf" /c/Linux/emarkaz-large-files-backup/
```

Then regenerate pages:

```bash
python generate_file_pages.py
```

Then commit and push:

```bash
git add -A

git commit -m "Add semester files without oversized PDF"

git push origin main
```

---

## 14. If Push Failed After Commit Because of Large File

If the commit happened locally but GitHub rejected the push, use this safe recovery process:

```bash
cd /c/Linux/emarkaz-course-library

git reset --soft HEAD~1

git restore --staged .

mkdir -p /c/Linux/emarkaz-large-files-backup

mv "books/ac-alim-course/semester-05/MusnadUlImamIlAazamAlBushraColor مسند الإمام الأعظم ابي حنيفة.pdf" /c/Linux/emarkaz-large-files-backup/

python generate_file_pages.py

git add -A

git commit -m "Add semester files without oversized PDF"

git push origin main
```

Explanation:

```text
git reset --soft HEAD~1
```

This removes the last local commit but keeps your files.

```text
git restore --staged .
```

This unstages everything.

Then we remove the oversized file, regenerate pages, commit again, and push.

---

## 15. Do Not Use Git LFS for GitHub Pages PDFs

Earlier, PDF open failed because PDFs were tracked by Git LFS.

The `.gitattributes` file had:

```text
*.pdf filter=lfs diff=lfs merge=lfs -text
```

This caused GitHub Pages to serve a pointer file instead of the real PDF file.

To stop tracking PDFs with Git LFS:

```bash
git lfs untrack "*.pdf"

git rm --cached -r books

git add .gitattributes

git add books

git commit -m "Serve PDFs directly without Git LFS"

git push origin main
```

Important rule:

```text
Do not use Git LFS for PDFs that need to open directly on GitHub Pages.
```

---

## 16. Final Rules

```text
PDF under 100 MB  → push to GitHub normally
PDF over 100 MB   → compress, split, or host elsewhere
Git LFS           → do not use for GitHub Pages PDFs
Empty folder      → add .gitkeep
New files added   → run generator and git add -A
```

---

## 17. Final Daily Workflow

Whenever new books/files are added:

```bash
cd /c/Linux/emarkaz-course-library

find books -type f -size +95M -print

python generate_file_pages.py

git status

git add -A

git commit -m "Add new course files and update pages"

git push origin main
```

Or simply run:

```bash
./upload.sh
```

---

## 18. Website Link

GitHub Pages site:

```text
https://krmaryum.github.io/emarkaz-course-library/
```

---

## 19. Summary

This project is now organized and semi-automated.

You can add files into any semester folder, run the generator, and push.

The website will show updated file cards automatically.

This saves time and prevents manual HTML editing for every new book.
