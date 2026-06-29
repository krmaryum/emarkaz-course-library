# How to Add Future Books

## Recommended Naming Rules

Use English folder and file names for safe GitHub Pages URLs.

Good:

```text
books/ac-alim-course/semester-01/fiqh-book-01.pdf
```

Avoid spaces and Urdu characters in the file path.

## Courses

```text
AC  = ac-alim-course
DC  = dc-ilm-e-deen-course
TIF = tif-takhasus-fil-ifta
TFA = tfa-takhasus-fil-aqaid
```

## Add a PDF

```bash
cp "/path/to/your book.pdf" books/ac-alim-course/semester-01/book-name.pdf
```

Then:

```bash
git add .
git commit -m "Add AC semester 01 book"
git push origin main
```

## Empty Folder Reminder

Git does not track empty folders. Keep `.gitkeep` inside folders until real PDFs are added.
