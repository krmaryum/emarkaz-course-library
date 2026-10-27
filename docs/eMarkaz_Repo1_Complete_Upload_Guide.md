# eMarkaz Course Library — Complete Upload & Publishing Guide

**Repository #1 (production):** `krmaryum/emarkaz-course-library`  
**Local Windows directory:** `C:\Linux\emarkaz-course-library`  
**Git Bash directory:** `/c/Linux/emarkaz-course-library`  
**Live website:** https://emarkazlibrary.com  
**GitHub Actions:** https://github.com/krmaryum/emarkaz-course-library/actions  
**Last updated:** October 27, 2026

> **Important:** This guide is for **Repo #1 only**. Do not confuse it with **Repo #2** (`/c/Linux/test-github-actions`, website `khalidkhan.me`).

## 1. The simple everyday workflow

1. Make the new folder **inside** `C:\Linux\emarkaz-course-library` and copy your PDFs there.
2. Check PDF size (preferably each file below **50 MB**; keep below the script's **95 MB** threshold and GitHub's 100 MB per-file limit).
3. Open **Git Bash** and go to the repo root:
   ```bash
   cd /c/Linux/emarkaz-course-library
   pwd
   ```
4. Run the existing helper:
   ```bash
   ./upload.sh
   ```
   (`bash upload.sh` also works.)
5. The script asks whether to add a **direct homepage button**. Answer `yes` only if you want that button on the **main homepage**. Otherwise answer `no`; nested folder pages still get generated automatically.
6. Enter a meaningful **commit message** when prompted. The script stages, commits, and pushes.
7. Open **GitHub Actions** and wait for **pages build and deployment** to show a **green check**. A successful `git push` alone does not mean the live site has deployed yet.
8. Refresh the website with **Ctrl + Shift + R** and test the homepage button, generated folder page, and PDF links.

## 2. Real example: add TIF Semester 03

Folder location:

```text
C:\Linux\emarkaz-course-library\books\tif-takhasus-fil-ifta\semester-03\
```

Example structure:

```text
emarkaz-course-library/
└── books/
    └── tif-takhasus-fil-ifta/
        ├── semester-01/
        ├── semester-02/
        └── semester-03/
            ├── book-one.pdf
            ├── book-two.pdf
            └── (...more books...)
```

Confirm in Git Bash:

```bash
cd /c/Linux/emarkaz-course-library
ls -la "books/tif-takhasus-fil-ifta/semester-03"
find "books/tif-takhasus-fil-ifta/semester-03" -type f -iname '*.pdf' -print
```

Run the publishing helper:

```bash
./upload.sh
```

### 2A. If Semester 03 should appear directly on the MAIN homepage

Respond to the interactive prompts exactly like this:

```text
Do you want to check/add a folder link to homepage? Type yes or no: yes
Enter folder path from repo root: books/tif-takhasus-fil-ifta/semester-03
Do you want to add this folder to homepage? Type yes or no: yes
Choose section number: 3
Enter custom button label, or press Enter to use suggested label: [PRESS ENTER]
Do you want to check another folder? Type yes or no: no
```

`3` is the **TIF section number**. It is **not** a folder path. The full relative folder path must be typed when the script asks for a folder path.

Expected homepage link:

```html
<a class="semester" href="books/tif-takhasus-fil-ifta/semester-03/">Semester 03</a>
```

Suggested commit message:

```text
Add TIF Semester 03 homepage button
```

After successful deployment:

- Homepage: https://emarkazlibrary.com/
- TIF Semester 03: https://emarkazlibrary.com/books/tif-takhasus-fil-ifta/semester-03/

### 2B. If folder should NOT appear as a direct homepage button

Answer `no` to:

```text
Do you want to check/add a folder link to homepage? Type yes or no: no
```

That is correct when you only want visitors to reach the new folder by navigating inside its parent course pages. The approved-root generator will create the nested `index.html` page and the parent folder will link to it.

**Remember:** `no` means **no new direct homepage button**; it does **not** mean "do not upload my PDFs".

## 3. Homepage helper section numbers

| Number | Homepage section |
|---|---|
| `1` | AC — Alim Course |
| `2` | DC — Ilm-e-Deen Course |
| `3` | TIF — Takhasus fil Ifta |
| `4` | TFA — Takhasus fil Aqaid |
| `5` | General Library |

The **folder path** is always relative to the repository root (the directory containing `upload.sh`). Do **not** enter a Windows drive path at this prompt. Do **not** put quotes around an interactive folder path, even if the name contains spaces. Example: `Molana-Ilyas-Ghuman-db-Books`.

## 4. What `upload.sh` does

Based on the current helper, it:

1. Confirms needed site files are present.
2. Checks for oversized files above 95 MB.
3. Adds `.gitkeep` to empty directories so Git can track them.
4. Optionally runs `homepage_link_helper.py` to add a main-homepage button.
5. Runs `generate_file_pages.py` to create/update folder `index.html` pages.
6. Shows Git status, stages all changes, asks for a commit message, commits and pushes to GitHub.

Running the generator directly is also useful for inspection:

```bash
python generate_file_pages.py
```

Your configured approved roots currently include:

```python
PUBLIC_LIBRARY_ROOTS = [
    "books",
    "emarkaz-books",
    "quran-juzz",
    "Fatawaz",
    "Molana-Ilyas-Ghuman-db-Books",
]
```

### Nested folder vs new TOP-LEVEL root

- **New folder under `books/`, `emarkaz-books/`, `quran-juzz/`, `Fatawaz/` or `Molana-Ilyas-Ghuman-db-Books/`**: usually no generator code change needed.
- **New top-level folder next to `books/`**: a homepage link is **not enough**. Add its exact name to `PUBLIC_LIBRARY_ROOTS` inside `generate_file_pages.py`, then generate and publish. Otherwise a 404 may occur because that folder has no generated `index.html`.

## 5. File size: GitHub and PDF safety

- **Below 50 MB per PDF:** preferred for fast use and fewer GitHub warnings.
- **50–100 MB:** GitHub warns for files larger than 50 MB; normal Git often still accepts them below 100 MB, but the repo becomes heavy.
- **Above the script's 95 MB threshold:** do not proceed through the helper; compress or split first.
- **100 MB or larger:** standard GitHub Git pushes reject oversized individual files.

Check for large files:

```bash
cd /c/Linux/emarkaz-course-library
find . -path './.git' -prune -o -type f -size +50M -print
find . -path './.git' -prune -o -type f -size +95M -print
```

**Note:** `find -size +50M` and `+95M` use 1 MiB blocks. They are screening commands, not precise byte comparisons. Your `upload.sh` has its own size check.

**Example:** A 109 MB original PDF was split into smaller files. Upload only the parts, not the original oversized file or an oversized ZIP. Keep the individual PDF parts in the correct course folder.

**Important:** Deleting a large PDF from your working folder later does not automatically remove it from Git history.

## 6. Verify that pages really exist

For TIF Semester 03:

```bash
cd /c/Linux/emarkaz-course-library
ls -l "books/tif-takhasus-fil-ifta/semester-03/index.html"
```

Check its parent folder page:

```bash
ls -l "books/tif-takhasus-fil-ifta/index.html"
```

Check whether your MAIN homepage contains the direct button:

```bash
grep -n 'books/tif-takhasus-fil-ifta/semester-03/' index.html
```

- If `grep` prints a matching line: main homepage link exists locally.
- If it prints nothing: run the homepage helper (via `./upload.sh`) and answer `yes` with the correct folder path and section.

## 7. How to confirm successful publication

Look for Git output similar to:

```text
[main fdb5a2e] Add TIF Semester 03 homepage button
To github.com:krmaryum/emarkaz-course-library.git
   726d4c7..fdb5a2e  main -> main
Done.
```

Then check:

**GitHub Actions:** https://github.com/krmaryum/emarkaz-course-library/actions

Find the latest **pages build and deployment** run for your commit. All of `build`, `report-build-status`, and `deploy` should show a **green check** and the overall status should say **Success**.

Only after the deployment succeeds, test:

1. https://emarkazlibrary.com/
2. https://emarkazlibrary.com/books/tif-takhasus-fil-ifta/semester-03/
3. Click a real PDF to verify it opens.

Force a browser refresh with **Ctrl + Shift + R** or try an Incognito window if the site appears old. It is normal for Pages deployment to take several minutes; do not make duplicate commits to hurry it along.

## 8. Troubleshooting

### Problem A: "ERROR: Folder does not exist: 3"

**Cause:** You typed the section number `3` into the **folder path** question.

**Fix:** When asked `Do you want to check another folder?`, answer `yes` and enter:

```text
books/tif-takhasus-fil-ifta/semester-03
```

Then answer `yes` to add the homepage button and choose section `3`. No need to restart the whole script.

### Problem B: New folder opens with GitHub Pages 404

**Likely causes:** Its `index.html` has not been generated or pushed, its URL/capitalization is wrong, or the Pages deployment has not finished.

Check:

```bash
cd /c/Linux/emarkaz-course-library
ls -l 'books/tif-takhasus-fil-ifta/semester-03/index.html'
git status
```

For a **new top-level folder**, also confirm it is included in `PUBLIC_LIBRARY_ROOTS`. Then run `./upload.sh`, check the green deployment, and retry the exact URL.

### Problem C: Push succeeded but new button is missing on homepage

1. Check homepage link locally:
   ```bash
   grep -n 'books/tif-takhasus-fil-ifta/semester-03/' index.html
   ```
2. Verify the push contained `index.html` (look at the GitHub commit).
3. Check the latest **GitHub Pages deployment** is green/successful.
4. Hard-refresh the website: **Ctrl + Shift + R**.
5. If deployment succeeded and the link is present in the published commit but missing live, inspect the deployed homepage source and Pages settings. Do not keep rerunning `upload.sh` without diagnosis.

**Real October 27, 2026 example:** Commit `fdb5a2e` successfully added the TIF Semester 03 homepage button. The main page initially showed the old two-button layout because Pages deployment **#108** was still running. After deployment #108 succeeded, the live page displayed all three semester buttons. This was a **deployment timing issue**, not a failed Git push.

### Problem D: `nothing to commit, working tree clean`

No local changes remain to commit. Check if your new PDFs were really copied into the repository folder, whether your URL button was already added, and whether the expected generated files exist. Do not force an empty commit unless you understand why.

### Problem E: File is above 95 MB / GitHub rejects a large file

Stop and split/compress the original PDF so each resulting file is preferably less than 50 MB. Copy only the resulting parts into the target folder; then run `./upload.sh` again.

### Problem F: An unexpected Windows/Git long-path error

Keep Unicode/Urdu names if needed. Check:

```bash
git config --global core.longpaths true
```

You may still need Windows Long Paths support or WSL for unusually deep paths. Avoid renaming course folders casually because published URLs depend on their names.

### Problem G: Already added homepage button; adding it again?

First verify:

```bash
grep -n 'books/tif-takhasus-fil-ifta/semester-03/' index.html
```

If present, choose `no` in the homepage helper for later ordinary PDF uploads; regenerating pages will update the book listings without duplicating homepage links.

## 9. Final checklist before and after every update

- [ ] I am in repo #1 (`/c/Linux/emarkaz-course-library`), **not** repo #2.
- [ ] PDFs are in the correct folder.
- [ ] Individual PDF sizes are reasonable (preferably under 50 MB).
- [ ] I did not accidentally include an original >100 MB PDF or oversized ZIP.
- [ ] I ran `./upload.sh`.
- [ ] I answered `yes` for homepage helper **only if a new direct homepage button is needed**.
- [ ] I supplied the full path relative to the repository root, not a section number.
- [ ] I picked the correct section (TIF = `3`).
- [ ] The generated folder's `index.html` exists.
- [ ] Git commit and push succeeded.
- [ ] GitHub Pages `pages build and deployment` is **Success**.
- [ ] I refreshed the site and tested the links and PDF files.

## 10. One-minute reminder: commands and rules

```bash
cd /c/Linux/emarkaz-course-library
pwd
ls -la 'books/tif-takhasus-fil-ifta/semester-03'
find 'books/tif-takhasus-fil-ifta/semester-03' -type f -iname '*.pdf' -print
./upload.sh
```

**Questions to remember:**

```text
Want a direct MAIN homepage button?  YES
Want only a nested folder/page?      NO
TIF section number?                  3
Folder path for TIF Semester 03?     books/tif-takhasus-fil-ifta/semester-03
Push succeeded, site not changed?    CHECK GITHUB PAGES DEPLOYMENT
```

---

**Suggested repo location for this guide:** `docs/eMarkaz_Repo1_Complete_Upload_Guide.md` or repository root. It is documentation only; it does not replace `upload.sh`, `homepage_link_helper.py`, or `generate_file_pages.py`.
