# eMarkaz Course Library

An organized, class-wise and semester-wise Urdu Islamic course library for PDF books and study materials.

**Live website:** https://emarkazlibrary.com  
**Repository:** https://github.com/krmaryum/emarkaz-course-library  
**GitHub Pages deployments:** https://github.com/krmaryum/emarkaz-course-library/actions

## Courses

| Code | English name | Urdu / Arabic name |
|---|---|---|
| AC | Alim Course | عالم کورس |
| DC | Ilm-e-Deen Course | علم دین کورس |
| TIF | Takhasus fil Ifta | تخصص فی الافتاء |
| TFA | Takhasus fil Aqaid | تخصص فی العقائد |

## Repository structure

```text
emarkaz-course-library/
├── assets/                        # Website assets
├── books/                         # Course and semester books
│   ├── ac-alim-course/
│   ├── dc-ilm-e-deen-course/
│   ├── tif-takhasus-fil-ifta/
│   │   ├── semester-01/
│   │   ├── semester-02/
│   │   └── semester-03/
│   └── tfa-takhasus-fil-aqaid/
├── emarkaz-books/                 # Additional eMarkaz collections
├── quran-juzz/                    # Quran Juzz
├── Fatawaz/                       # Fatawa collection
├── Molana-Ilyas-Ghuman-db-Books/  # Books organized by topic
├── docs/                          # Repository operating guides
│   ├── README.md
│   └── eMarkaz_Repo1_Complete_Upload_Guide.md
├── index.html                     # Main homepage
├── generate_file_pages.py         # Builds library folder pages
├── homepage_link_helper.py        # Adds selected homepage links
├── upload.sh                       # Guided generate/commit/push workflow
└── CNAME                           # Custom domain
```

This is a **representative** tree; nested semester folders, books, and other repository files are omitted for readability.

## Everyday workflow: add PDF books or a semester

1. Place PDF files into the correct folder under `C:\Linux\emarkaz-course-library`. For example:
   `books/tif-takhasus-fil-ifta/semester-03/`.
2. Check file sizes. Prefer PDFs smaller than 50 MB. GitHub warns for individual files above 50 MB and blocks ordinary Git files above 100 MB; the repository upload helper checks for files over 95 MB. Split or optimize oversized PDFs **before** adding them to Git.
3. Open Git Bash and work from the repository root:

   ```bash
   cd /c/Linux/emarkaz-course-library
   git status
   ./upload.sh
   ```

4. At the **homepage link helper** prompt:
   - Answer **`yes`** if you want a **direct homepage button**. Enter the folder path **relative to the repository root**, such as `books/tif-takhasus-fil-ifta/semester-03`, then choose its section (`3` for TIF), and accept or edit the label.
   - Answer **`no`** if you only need the folder listed on its parent library page; the generator handles folders within approved roots automatically.
5. Enter a meaningful commit message when requested, such as `Add TIF Semester 03 books and homepage link`.
6. Confirm that `git push` finished successfully. **A successful push does not mean Pages deployment has finished.**
7. Check [GitHub Actions](https://github.com/krmaryum/emarkaz-course-library/actions) for a successful **pages build and deployment**, then open https://emarkazlibrary.com and refresh with `Ctrl + Shift + R` if necessary.

> **Example:** For the TIF Semester 03 homepage button, use folder path `books/tif-takhasus-fil-ifta/semester-03` and homepage section **3 (TIF)**. Do not type `3` when the helper asks for a folder path.

## How the site is generated

The `generate_file_pages.py` script creates `index.html` files for folders inside the following approved public library roots:

```python
PUBLIC_LIBRARY_ROOTS = [
    "books",
    "emarkaz-books",
    "quran-juzz",
    "Fatawaz",
    "Molana-Ilyas-Ghuman-db-Books",
]
```

If you create a **new top-level** library collection outside this list, add its root name to `PUBLIC_LIBRARY_ROOTS` before regenerating pages. Otherwise its homepage link may lead to a **404** because its folder has no generated `index.html`.

For a new semester **inside `books/`**, you do **not** need to change the approved roots.

## Sync local files after changes made on GitHub.com

If you create/edit/upload files directly in GitHub's web interface, update your local copy **before your next local upload**:

```bash
cd /c/Linux/emarkaz-course-library
git status
git pull --ff-only origin main
git status
```

`--ff-only` is suitable when your local branch has no divergent commits; it stops rather than creating a merge or rewriting commits. If branches have diverged, inspect the history before deciding whether `git pull --rebase origin main` is appropriate. For a clean local branch, the first `git status` should report no uncommitted changes.

## File names and empty folders

- Use clear, descriptive file names. **Urdu and Arabic file names are supported**; there is no need to rename existing books just to make them English.
- Avoid unnecessarily deep folder paths that can trigger Windows path-length problems.
- Git does not track empty folders. The upload helper adds `.gitkeep` to empty folders so their structure can be committed.
- Avoid duplicate PDF copies and do not commit original PDFs larger than GitHub's standard per-file limit.

## Documentation

- [Complete upload and publishing guide](docs/eMarkaz_Repo1_Complete_Upload_Guide.md) — detailed step-by-step operations and troubleshooting.
- [Documentation folder](docs/) — additional how-to notes and guides.

## Troubleshooting quick reference

| Symptom | What to check |
|---|---|
| New button missing on homepage | Did you answer `yes` in the homepage helper, choose the correct course section, commit/push, and confirm the Pages deployment succeeded? |
| Folder URL returns 404 | Does the folder contain a generated `index.html`? Is it under an approved public root? Was the generated page pushed? |
| Git push succeeded but live site still looks old | Check the latest **pages build and deployment** run; refresh browser only after it succeeds. |
| File too large | Split or compress PDF before adding to Git; prefer each part under 50 MB. |
| Git pull refuses to fast-forward | Check `git status` and `git log --oneline --graph --decorate --all -10` before deciding how to reconcile branches. |

For full examples and recovery procedures, use the [complete upload guide](docs/eMarkaz_Repo1_Complete_Upload_Guide.md).

---

**Scope:** This README describes **Repo #1 (production eMarkaz library)**. It is separate from the `test-github-actions` practice repository and `khalidkhan.me` website.
