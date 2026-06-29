# eMarkaz Course Library

A class-wise and semester-wise Urdu Islamic course library with PDF books and study materials.

## Courses

| Code | English Name | Urdu / Arabic Name |
|---|---|---|
| AC | Alim Course | عالم کورس |
| DC | Ilm-e-Deen Course | علم دین کورس |
| TIF | Takhasus fil Ifta | تخصص فی الافتاء |
| TFA | Takhasus fil Aqaid | تخصص فی العقائد |

## Folder Structure

```text
books/
├── ac-alim-course/
│   ├── semester-01/
│   ├── semester-02/
│   └── semester-08/
├── dc-ilm-e-deen-course/
├── tif-takhasus-fil-ifta/
└── tfa-takhasus-fil-aqaid/
```

## Important Git Note

Git does not track empty folders. A `.gitkeep` file is included inside empty semester folders so the folder structure appears on GitHub.

## Add a New PDF Book

1. Copy the PDF into the correct semester folder.
2. Use English lowercase filenames with hyphens.

Example:

```text
books/ac-alim-course/semester-01/aqeedah-book.pdf
```

3. Commit and push:

```bash
git add .
git commit -m "Add new course books"
git push origin main
```

## GitHub Pages

The site is published from the `main` branch using GitHub Pages.
