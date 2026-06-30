# eMarkaz Course Library

A class-wise and semester-wise Urdu Islamic course library with PDF books and study materials.

## Project Purpose

This project is created to organize religious course books in a clean online library. Students can open and download PDF books according to course, class, and semester.

The website will be hosted using GitHub Pages.

## Courses

| Code | English Name | Urdu Name |
|---|---|---|
| AC | Alim Course | عالم کورس |
| DC | Ilm-e-Deen Course | علم دین کورس |
| TIF | Takhasus fil Ifta | تخصص فی الافتاء |
| TFA | Takhasus fil Aqaid | تخصص فی العقائد |

## Recommended Folder Structure

```text
emarkaz-course-library/
├── README.md
├── index.html
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
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
    ├── dc-ilm-e-deen-course/
    │   ├── semester-01/
    │   ├── semester-02/
    │   ├── semester-03/
    │   └── semester-04/
    ├── tif-takhasus-fil-ifta/
    │   ├── semester-01/
    │   └── semester-02/
    └── tfa-takhasus-fil-aqaid/
        ├── semester-01/
        └── semester-02/
```

## Important GitHub Note

Git does not track empty folders. If a semester folder has no PDF yet, add a `.gitkeep` file inside it.

Example:

```bash
touch books/ac-alim-course/semester-01/.gitkeep
```

To add `.gitkeep` to all empty folders:

```bash
find books -type d -empty -exec touch {}/.gitkeep \;
```

## Create Folder Structure

Run these commands from the project root:

```bash
mkdir -p assets/css assets/js assets/images

mkdir -p books/ac-alim-course/semester-01
mkdir -p books/ac-alim-course/semester-02
mkdir -p books/ac-alim-course/semester-03
mkdir -p books/ac-alim-course/semester-04
mkdir -p books/ac-alim-course/semester-05
mkdir -p books/ac-alim-course/semester-06
mkdir -p books/ac-alim-course/semester-07
mkdir -p books/ac-alim-course/semester-08

mkdir -p books/dc-ilm-e-deen-course/semester-01
mkdir -p books/dc-ilm-e-deen-course/semester-02
mkdir -p books/dc-ilm-e-deen-course/semester-03
mkdir -p books/dc-ilm-e-deen-course/semester-04

mkdir -p books/tif-takhasus-fil-ifta/semester-01
mkdir -p books/tif-takhasus-fil-ifta/semester-02

mkdir -p books/tfa-takhasus-fil-aqaid/semester-01
mkdir -p books/tfa-takhasus-fil-aqaid/semester-02
```

## Add Placeholder Files

```bash
find books -type d -empty -exec touch {}/.gitkeep \;
```

## Add PDF Books

Use English file names for clean GitHub Pages links.

Good example:

```text
books/ac-alim-course/semester-01/aqeedah-book.pdf
```

Avoid spaces and special characters in file names.

Better:

```text
aqaid-book.pdf
fiqh-book.pdf
seerah-book.pdf
hadith-book.pdf
```

Not recommended:

```text
Aqeedah Book Final New Copy.pdf
```

## Website Link Example

```html
<a href="books/ac-alim-course/semester-01/aqeedah-book.pdf" target="_blank">
  کتاب کھولیں
</a>

<a href="books/ac-alim-course/semester-01/aqeedah-book.pdf" download>
  ڈاؤن لوڈ کریں
</a>
```

## Git Commands

After adding files or folders:

```bash
git status
git add .
git commit -m "Add course library structure"
git push origin main
```

## GitHub Pages Setup

1. Go to the GitHub repository.
2. Open **Settings**.
3. Click **Pages**.
4. Under **Build and deployment**, choose:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/root`
5. Save.

After deployment, the website will be available at:

```text
https://krmaryum.github.io/emarkaz-course-library/
```

## Future Plan

Later, this project can include:

- Course cards
- Semester pages
- PDF open/download buttons
- Urdu/Arabic interface
- Search option
- Mobile-friendly layout
- Teacher notes section
- Student resources section

## Languages

The folder and file names should stay in English for clean URLs.

The website content can show Urdu, Arabic, and Roman Urdu.

Example website labels:

```text
کتاب کھولیں
ڈاؤن لوڈ کریں
سمسٹر اول
عالم کورس
علم دین کورس
تخصص فی الافتاء
تخصص فی العقائد
```

## Project Description

Roman Urdu:

```text
Class-wise aur semester-wise Urdu Islami course library jisme PDF books aur study materials shamil hain.
```

Urdu:

```text
کلاس وار اور سمسٹر وار اردو اسلامی کورس لائبریری، جس میں پی ڈی ایف کتابیں اور مطالعاتی مواد شامل ہے۔
```

Arabic:

```text
مكتبة دورة إسلامية باللغة الأردية، منظمة حسب الصفوف والفصول الدراسية، وتحتوي على كتب بصيغة PDF ومواد دراسية.
```
