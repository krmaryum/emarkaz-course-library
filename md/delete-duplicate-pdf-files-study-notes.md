# Study Notes: Delete Duplicate `(1).pdf` Files Before Uploading to eMarkaz Library

## Purpose

These notes explain how to safely find and delete duplicate PDF files that end with:

```text
(1).pdf
```

This commonly happens when files are downloaded more than once or copied from Google Drive/ZIP folders.

Example duplicate files:

```text
book-name(1).pdf
فتاویٰ کتاب(1).pdf
2623ستائیس رجب کو روزہ رکھنا کیسا ہے؟(1).pdf
```

---

## 1. Why These Files Should Be Deleted

Files ending with `(1).pdf` are usually duplicate copies.

Example:

```text
2623ستائیس رجب کو روزہ رکھنا کیسا ہے؟.pdf
2623ستائیس رجب کو روزہ رکھنا کیسا ہے؟(1).pdf
```

The second file is normally a duplicate.

Keeping duplicates can create:

```text
Extra storage usage
Duplicate book cards on the website
Confusion for users
Larger Git repository size
Longer upload time
```

---

## 2. Important Safety Rule

Always preview files first before deleting.

Do this first:

```bash
find . -maxdepth 1 -type f -name "*(1).pdf" -print
```

Only after checking the output, delete them:

```bash
find . -maxdepth 1 -type f -name "*(1).pdf" -delete
```

---

## 3. Command Explanation

Command:

```bash
find . -maxdepth 1 -type f -name "*(1).pdf" -print
```

Meaning:

| Part | Meaning |
|---|---|
| `find` | Search files/folders |
| `.` | Search in current folder |
| `-maxdepth 1` | Only search current folder, not inside subfolders |
| `-type f` | Search files only |
| `-name "*(1).pdf"` | Match files ending with `(1).pdf` |
| `-print` | Show matching files |

---

## 4. Delete Command Explanation

Command:

```bash
find . -maxdepth 1 -type f -name "*(1).pdf" -delete
```

Meaning:

| Part | Meaning |
|---|---|
| `find .` | Search current folder |
| `-maxdepth 1` | Do not go inside subfolders |
| `-type f` | Files only |
| `-name "*(1).pdf"` | Match duplicate PDFs |
| `-delete` | Delete matched files |

---

## 5. Safe Workflow Inside Repo Folder

Example repo folder:

```bash
cd /c/Linux/emarkaz-course-library/Fatawaz
```

### Step 1: Preview duplicate files

```bash
find . -maxdepth 1 -type f -name "*(1).pdf" -print
```

### Step 2: Delete duplicate files

```bash
find . -maxdepth 1 -type f -name "*(1).pdf" -delete
```

### Step 3: Confirm deletion

```bash
find . -maxdepth 1 -type f -name "*(1).pdf" -print
```

If nothing is printed, the duplicate files are deleted successfully.

---

## 6. Safe Workflow Inside Downloads Folder

Example Downloads folder:

```bash
cd ~/Downloads/فتاویٰ\ مرکز\ اھل\ السنۃ\ والجماعۃ-20260702T044635Z-3-001/فتاویٰ\ مرکز\ اھل\ السنۃ\ والجماعۃ
```

Preview duplicates:

```bash
find . -maxdepth 1 -type f -name "*(1).pdf" -print
```

Delete duplicates:

```bash
find . -maxdepth 1 -type f -name "*(1).pdf" -delete
```

Confirm:

```bash
find . -maxdepth 1 -type f -name "*(1).pdf" -print
```

If nothing appears, the folder is clean.

---

## 7. Copy Clean PDFs From Downloads to Repo

After cleaning the Downloads folder, copy the PDFs into the repo folder.

Go to repo folder:

```bash
cd /c/Linux/emarkaz-course-library/Fatawaz
```

Copy PDFs:

```bash
cp -v ~/Downloads/فتاویٰ\ مرکز\ اھل\ السنۃ\ والجماعۃ-20260702T044635Z-3-001/فتاویٰ\ مرکز\ اھل\ السنۃ\ والجماعۃ/*.pdf .
```

---

## 8. Upload Changes to GitHub

Go back to repo root:

```bash
cd /c/Linux/emarkaz-course-library
```

Run upload script:

```bash
./upload.sh
```

When homepage helper asks:

```text
Do you want to check/add a folder link to homepage?
```

Type:

```text
no
```

Suggested commit message:

```text
Remove duplicate Fatawaz PDFs
```

or:

```text
Update Fatawaz PDFs
```

---

## 9. Check Git Status

After upload:

```bash
git status
```

Expected output:

```text
nothing to commit, working tree clean
```

This means your repo is clean and updated.

---

## 10. One-Line Safe Flow for Repo Folder

```bash
cd /c/Linux/emarkaz-course-library/Fatawaz
find . -maxdepth 1 -type f -name "*(1).pdf" -print
find . -maxdepth 1 -type f -name "*(1).pdf" -delete
find . -maxdepth 1 -type f -name "*(1).pdf" -print
cd /c/Linux/emarkaz-course-library
./upload.sh
```

---

## 11. Best Practice

Before uploading any new PDF folder:

```bash
find . -maxdepth 1 -type f -name "*(1).pdf" -print
```

If it prints duplicate files, delete them before copying or uploading.

---

## 12. Important Warning

Do not use broad delete commands like:

```bash
rm *.pdf
```

unless you really want to delete all PDF files.

For duplicate files only, use:

```bash
find . -maxdepth 1 -type f -name "*(1).pdf" -delete
```

This is safer and more specific.

---

## 13. Final Memory Line

```text
Preview first, delete second, confirm third, then upload.
```

Alhamdulillah, this keeps the eMarkaz Library clean and avoids duplicate book files.
