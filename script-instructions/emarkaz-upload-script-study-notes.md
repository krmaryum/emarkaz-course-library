# eMarkaz `upload.sh` Script — Study Notes

## Purpose

The `upload.sh` script is an automation script for the eMarkaz Course Library project.

Instead of running many commands manually every time, you can add folders or files and then run one script:

```bash
./upload.sh
```

The script will generate website pages, stage changes, commit them, and push them to GitHub.

---

## Repository Location

Your eMarkaz repository is located here:

```bash
/c/Linux/emarkaz-course-library
```

The script uses this path:

```bash
REPO_DIR="/c/Linux/emarkaz-course-library"
```

---

## Main Workflow

The simple workflow is:

```text
Add folders/files → run ./upload.sh → website updates
```

---

## Supported Main Folders

The script is designed for these folders:

```text
books/
emarkaz-books/
quran-juzz/
```

---

## What You Can Add

You can add:

```text
new folders
nested folders
PDF books
DOCX files
Markdown files
Excel files
```

Supported file types depend on `generate_file_pages.py`:

```text
.pdf
.docx
.md
.xlsx
.xls
```

---

## Folder Support

### Course/Semester Folders

Example:

```text
books/ac-alim-course/semester-09/
books/dc-ilm-e-deen-course/semester-06/
books/tif-takhasus-fil-ifta/semester-02/
```

### Nested Semester Folders

Example:

```text
books/ac-alim-course/semester-08/Exam Papers/
books/ac-alim-course/semester-09/Assignments/
books/ac-alim-course/semester-10/Notes/
```

### General eMarkaz Books Folders

Example:

```text
emarkaz-books/e-courses/fiqh/
emarkaz-books/e-courses/hadith/
emarkaz-books/e-courses/grammar/nawh/
```

### Quran Juzz Folders

Example:

```text
quran-juzz/
quran-juzz/para-01/
quran-juzz/translation/
```

---

## What the Script Does

The script performs these steps:

```text
1. Goes to the eMarkaz repository.
2. Checks that generate_file_pages.py exists.
3. Checks for large files above 95 MB.
4. Adds .gitkeep to empty folders.
5. Runs generate_file_pages.py.
6. Shows git status.
7. Runs git add -A.
8. Stops safely if there are no changes.
9. Asks for a commit message.
10. Commits the changes.
11. Pushes to GitHub main branch.
```

---

## Why `.gitkeep` Is Added

Git does not track empty folders.

So if you create a folder but it has no files, Git will ignore it.

The script fixes this by running:

```bash
find books emarkaz-books quran-juzz -type d -empty -exec touch {}/.gitkeep \; 2>/dev/null || true
```

This creates a small `.gitkeep` file inside empty folders so Git can track them.

---

## Large File Check

GitHub blocks files larger than 100 MB.

The script checks for files larger than 95 MB:

```bash
find books emarkaz-books quran-juzz -type f -size +95M
```

If it finds large files, it warns you before pushing.

Recommended file size:

```text
Under 50 MB      Best
50–100 MB        Warning zone
Over 100 MB      GitHub push will fail
```

---

## Normal Usage

First go to the repo:

```bash
cd /c/Linux/emarkaz-course-library
```

Then run:

```bash
./upload.sh
```

---

## First-Time Setup

After replacing or downloading the script, make it executable:

```bash
cd /c/Linux/emarkaz-course-library
chmod +x upload.sh
```

Then run:

```bash
./upload.sh
```

---

## Example 1: Add a New PDF Book

Copy your PDF into the correct folder:

```bash
cd /c/Linux/emarkaz-course-library

cp "/c/Users/krmar/Downloads/my-book.pdf" "emarkaz-books/e-courses/fiqh/"
```

Run the script:

```bash
./upload.sh
```

---

## Example 2: Add a New Nested Folder

Create the folder:

```bash
cd /c/Linux/emarkaz-course-library

mkdir -p "books/ac-alim-course/semester-08/Exam Papers"
```

Run the script:

```bash
./upload.sh
```

The script will add `.gitkeep`, generate pages, commit, and push.

---

## Example 3: Add a New Quran Juzz File

```bash
cd /c/Linux/emarkaz-course-library

cp "/c/Users/krmar/Downloads/para-01.pdf" "quran-juzz/"
./upload.sh
```

---

## Example 4: Add a New Semester Folder

```bash
cd /c/Linux/emarkaz-course-library

mkdir -p books/ac-alim-course/semester-11
./upload.sh
```

The generator will create:

```text
books/ac-alim-course/semester-11/index.html
```

Important:

If you want Semester 11 to appear on the homepage, you must also add its link in `index.html`.

Example:

```html
<a class="semester" href="books/ac-alim-course/semester-11/">Semester 11</a>
```

Then run:

```bash
./upload.sh
```

---

## When Homepage Update Is Needed

You do not need to update homepage for every file.

### No Homepage Update Needed

```text
Adding a PDF book
Adding a DOCX file
Adding a Markdown file
Adding a nested folder
Adding files inside emarkaz-books/
Adding files inside quran-juzz/
```

### Homepage Update Needed

```text
Adding a new semester that should show as a homepage button
Adding a brand-new main section
Changing homepage design
```

---

## Commit Message

The script asks:

```text
Enter custom commit message, or press Enter to use default:
```

You can type something clear:

```text
Add new Quran Juzz files
```

or press Enter to use the default:

```text
Add books and update library pages
```

---

## If There Are No Changes

The script will show:

```text
No changes to commit.
Nothing was pushed.
```

This is safe. It means there was nothing new to upload.

---

## Best Memory Line

```text
Add folders/files → run ./upload.sh → enter commit message → website updates
```

---

## Best Command to Remember

```bash
cd /c/Linux/emarkaz-course-library
./upload.sh
```

---

## Final Check

After push, wait a short time and check:

```text
https://emarkazlibrary.com
```

Common pages:

```text
https://emarkazlibrary.com/emarkaz-books/
https://emarkazlibrary.com/quran-juzz/
https://emarkazlibrary.com/books/ac-alim-course/semester-09/
```

Alhamdulillah, this script makes your eMarkaz upload workflow clean, repeatable, and easier to manage.
