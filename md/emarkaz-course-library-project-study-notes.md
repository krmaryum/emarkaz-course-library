# eMarkaz Course Library Project – Study Notes

## Project Goal

The goal of this project is to create a clean website for a religious course library where PDF books can be uploaded and organized course-wise, class-wise, and semester-wise.

This project will be hosted on GitHub Pages and will allow students to open or download PDF books easily.

---

## Repository Name

Recommended repository name:

```text
emarkaz-course-library
```

Possible description:

```text
A class-wise and semester-wise Urdu Islamic course library with PDF books and study materials.
```

Urdu description:

```text
کلاس وار اور سمسٹر وار اردو اسلامی کورس لائبریری، جس میں پی ڈی ایف کتابیں اور مطالعاتی مواد شامل ہے۔
```

Roman Urdu description:

```text
Class-wise aur semester-wise Urdu Islami course library jisme PDF books aur study materials shamil hain.
```

Arabic description:

```text
مكتبة دورة إسلامية باللغة الأردية، منظمة حسب الصفوف والفصول الدراسية، وتحتوي على كتب بصيغة PDF ومواد دراسية.
```

---

## Main Courses

| Code | English Name | Urdu / Arabic Name |
|---|---|---|
| AC | Alim Course | عالم کورس |
| DC | Ilm-e-Deen Course | علم دین کورس |
| TIF | Takhasus fil Ifta | تخصص فی الافتاء |
| TFA | Takhasus fil Aqaid | تخصص فی العقائد |

> Note: For folder names, use English lowercase names with hyphens. On the website, display names can be in Urdu.

---

## Recommended Folder Structure

```text
emarkaz-course-library/
│
├── index.html
├── README.md
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
│
└── books/
    ├── ac-alim-course/
    │   ├── semester-01/
    │   ├── semester-02/
    │   ├── semester-03/
    │   ├── semester-04/
    │   ├── semester-05/
    │   ├── semester-06/
    │   ├── semester-07/
    │   └── semester-08/
    │
    ├── dc-ilm-e-deen-course/
    │   ├── semester-01/
    │   ├── semester-02/
    │   ├── semester-03/
    │   └── semester-04/
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

## Why Use English Folder Names?

Use English folder and file names because they are safer for GitHub Pages URLs.

Good example:

```text
books/ac-alim-course/semester-01/aqeedah-book.pdf
```

Avoid using spaces or Urdu text in file paths when possible:

```text
books/عالم کورس/سمسٹر اول/عقیدہ کتاب.pdf
```

Urdu names can still be shown beautifully on the website, but folder/file paths should stay simple.

---

## Basic Commands Used

### 1. Clone Repository

```bash
git clone git@github.com:krmaryum/emarkaz-course-library.git
```

If the repository is empty, Git may show:

```text
warning: You appear to have cloned an empty repository.
```

This is normal. It means there are no files yet.

---

### 2. Go Inside the Repository

```bash
cd emarkaz-course-library
```

Check current location:

```bash
pwd
```

Check repository status:

```bash
git status
```

---

### 3. Create Basic Website Files

```bash
mkdir -p assets/css assets/js assets/images books
touch index.html README.md
```

Check files:

```bash
ls -l
```

---

## Create Course Folders

From the repository root:

```bash
mkdir -p books/ac-alim-course
mkdir -p books/dc-ilm-e-deen-course
mkdir -p books/tif-takhasus-fil-ifta
mkdir -p books/tfa-takhasus-fil-aqaid
```

Check:

```bash
ls -l books
```

Expected folders:

```text
ac-alim-course/
dc-ilm-e-deen-course/
tif-takhasus-fil-ifta/
tfa-takhasus-fil-aqaid/
```

---

## Create Semester Folders

From inside the `books` folder or from the repo root, create semester folders.

### AC – Alim Course

```bash
mkdir -p books/ac-alim-course/semester-01
mkdir -p books/ac-alim-course/semester-02
mkdir -p books/ac-alim-course/semester-03
mkdir -p books/ac-alim-course/semester-04
mkdir -p books/ac-alim-course/semester-05
mkdir -p books/ac-alim-course/semester-06
mkdir -p books/ac-alim-course/semester-07
mkdir -p books/ac-alim-course/semester-08
```

### DC – Ilm-e-Deen Course

```bash
mkdir -p books/dc-ilm-e-deen-course/semester-01
mkdir -p books/dc-ilm-e-deen-course/semester-02
mkdir -p books/dc-ilm-e-deen-course/semester-03
mkdir -p books/dc-ilm-e-deen-course/semester-04
```

### TIF – Takhasus fil Ifta

```bash
mkdir -p books/tif-takhasus-fil-ifta/semester-01
mkdir -p books/tif-takhasus-fil-ifta/semester-02
```

### TFA – Takhasus fil Aqaid

```bash
mkdir -p books/tfa-takhasus-fil-aqaid/semester-01
mkdir -p books/tfa-takhasus-fil-aqaid/semester-02
```

---

## Important Git Note: Empty Folders

Git and GitHub do **not** track empty folders.

If a folder has no file inside it, Git will ignore it.

### Solution: Use `.gitkeep`

A `.gitkeep` file is a small placeholder file used to keep empty folders in Git.

Run this command from repo root:

```bash
find books -type d -empty -exec touch {}/.gitkeep \;
```

This will create `.gitkeep` in every empty folder.

Check all `.gitkeep` files:

```bash
find books -name ".gitkeep"
```

---

## Add PDF Books Later

When a PDF book is ready, place it inside the correct course and semester folder.

Example:

```text
books/ac-alim-course/semester-01/aqeedah-book.pdf
```

Website button example:

```html
<a href="books/ac-alim-course/semester-01/aqeedah-book.pdf" target="_blank">
  کتاب کھولیں
</a>

<a href="books/ac-alim-course/semester-01/aqeedah-book.pdf" download>
  ڈاؤن لوڈ کریں
</a>
```

---

## Commit and Push Changes

After creating files and folders:

```bash
git status
git add .
git commit -m "Create course library folder structure"
git push origin main
```

---

## GitHub Pages Setup

After pushing files, enable GitHub Pages:

1. Go to GitHub repository
2. Click **Settings**
3. Click **Pages**
4. Under **Build and deployment**, select:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/root`
5. Save

After deployment, the website will be available at:

```text
https://krmaryum.github.io/emarkaz-course-library/
```

---

## Website Display Plan

Homepage should show four main course cards:

```text
AC - عالم کورس
Alim Course

DC - علم دین کورس
Ilm-e-Deen Course

TIF - تخصص فی الافتاء
Takhasus fil Ifta

TFA - تخصص فی العقائد
Takhasus fil Aqaid
```

Each course page or section can show semesters:

```text
سمسٹر 01
سمسٹر 02
سمسٹر 03
سمسٹر 04
```

Each semester can show book cards:

```text
Book Title
Open PDF
Download PDF
```

---

## Best Practices

### Use clean filenames

Good:

```text
aqeedah-book.pdf
fiqh-basics.pdf
hadith-notes.pdf
```

Avoid:

```text
Aqeedah Book Final New Copy 2026 (1).pdf
```

### Use lowercase and hyphens

Good:

```text
ilm-e-deen-book.pdf
```

Avoid:

```text
Ilm e Deen Book.pdf
```

### Keep one clear structure

Do not mix PDFs randomly in the root folder. Always place books inside:

```text
books/course-name/semester-name/
```

---

## Future Improvement Ideas

Later, the website can include:

- Urdu/Arabic RTL layout
- Course-wise search
- Semester filters
- PDF open/download buttons
- Teacher information
- Course introduction page
- Mobile-friendly cards
- Dark/light mode
- Contact section

---

## Summary

This project is a GitHub Pages website for an Urdu Islamic course library. It organizes books by course and semester. English folder names are used for clean URLs, while Urdu and Arabic names are displayed on the website. Since Git does not track empty folders, `.gitkeep` files are used until real PDF books are added.
