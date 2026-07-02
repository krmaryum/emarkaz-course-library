# eMarkaz Flexible Homepage Link Helper README

## Purpose

This workflow lets you create folders yourself first.

Then the upload script asks if you want to add any folder link to the homepage.

This is more flexible because the script is not limited only to semester folders.

---

## Files

Use these files in the repo root:

```text
generate_file_pages.py
homepage_link_helper.py
upload.sh
```

Repo root:

```text
/c/Linux/emarkaz-course-library
```

---

## Main Idea

```text
You create folder yourself
Run ./upload.sh
Script asks if you want to add a folder link to homepage
You provide folder path from repo root
Script verifies folder exists
Script asks which homepage section
Script adds button if you say yes
Script generates pages
Script commits and pushes
```

---

## Install

Copy the files into your repo root:

```bash
cd /c/Linux/emarkaz-course-library

cp /c/Users/krmar/Downloads/homepage_link_helper.py homepage_link_helper.py
cp /c/Users/krmar/Downloads/upload-flexible-homepage-helper.sh upload.sh

chmod +x upload.sh
```

---

## Normal Workflow

```bash
cd /c/Linux/emarkaz-course-library

# Create folders/files yourself first

./upload.sh
```

---

## Example 1: Add New Semester

Create folder:

```bash
cd /c/Linux/emarkaz-course-library
mkdir -p books/ac-alim-course/semester-11
```

Run:

```bash
./upload.sh
```

When asked:

```text
Do you want to check/add a folder link to homepage? Type yes or no:
```

Type:

```text
yes
```

When asked for folder path:

```text
books/ac-alim-course/semester-11
```

When asked to add homepage link:

```text
yes
```

Choose section:

```text
1
```

This means:

```text
AC - Alim Course
```

The script adds:

```html
<a class="semester" href="books/ac-alim-course/semester-11/">Semester 11</a>
```

---

## Example 2: Add eMarkaz Books Folder to Homepage

Create folder:

```bash
cd /c/Linux/emarkaz-course-library
mkdir -p emarkaz-books/e-courses/seerah
```

Run:

```bash
./upload.sh
```

Folder path to enter:

```text
emarkaz-books/e-courses/seerah
```

Choose homepage section:

```text
5
```

This means:

```text
General Library
```

Suggested label:

```text
Seerah
```

You can press Enter to use it.

---

## Example 3: Add Folder but Do Not Add Homepage Button

Create folder:

```bash
mkdir -p emarkaz-books/e-courses/private-notes
```

Run:

```bash
./upload.sh
```

When asked:

```text
Do you want to add this folder to homepage?
```

Type:

```text
no
```

The folder page can still be generated, but no homepage button is added.

---

## Example 4: Add Multiple Homepage Links in One Run

The helper will ask:

```text
Do you want to check another folder?
```

Type:

```text
yes
```

Then enter another folder path.

When finished, type:

```text
no
```

---

## Homepage Section Choices

The helper currently supports these homepage sections:

```text
1) AC - Alim Course
2) DC - Ilm-e-Deen Course
3) TIF - Takhasus fil Ifta
4) TFA - Takhasus fil Aqaid
5) General Library
```

---

## Important

The folder path must be from repo root.

Correct:

```text
books/ac-alim-course/semester-11
emarkaz-books/e-courses/seerah
quran-juzz/para-01
```

Wrong:

```text
/c/Linux/emarkaz-course-library/books/ac-alim-course/semester-11
```

---

## Supported Generated Pages

The generator still creates pages for:

```text
books/
emarkaz-books/
quran-juzz/
```

If you create a completely new root folder, the homepage helper can add a homepage link, but `generate_file_pages.py` will not automatically generate nested pages for that new root folder unless the generator is updated.

---

## Best Memory Line

```text
Create folder yourself → run ./upload.sh → provide folder path if homepage link is needed → push
```

---

## Best Command

```bash
cd /c/Linux/emarkaz-course-library
./upload.sh
```
