# eMarkaz Hadith Search — Install & Future Collections

This package creates a **single searchable library** from all PDF files in
`emarkaz-books/e-courses/hadith/`, including both Bukhari and Muslim.

## Install once (Git Bash, from repo root)

Copy these 3 files from the ZIP into the **repo root**:
- `build_hadith_search.py`
- `install_hadith_search_hook.py`
- `hadith-search.html` must go in `emarkaz-books/e-courses/hadith/` (NOT the root).

Run:

```bash
cd /c/Linux/emarkaz-course-library
python install_hadith_search_hook.py
python generate_file_pages.py
python build_hadith_search.py

git status
git add generate_file_pages.py build_hadith_search.py emarkaz-books/e-courses/hadith
# installation helper itself is optional to commit
git commit -m "Add expandable Hadith PDF search across all collections"
git push origin main
```

`generate_file_pages.py` will automatically rebuild the search index on later runs.
`upload.sh` already runs the generator, so future uploads can follow the usual workflow.

## Add a future collection

Create a new first-level folder in `emarkaz-books/e-courses/hadith/`, for example
`Sunan_Abi_Dawud/`, and put PDFs in any nested volume folders. Run `./upload.sh`.
The index will discover the new collection and all PDFs, create the search filter,
and add a search button to that collection's generated index page.

Optional: Give the new collection an Urdu display name by adding an entry in
`COLLECTION_NAMES` near the top of `build_hadith_search.py`.

## Search behavior

- Searches PDF filenames (and derived titles), across all discovered collections
- Urdu/Arabic/Roman Urdu/English matching with common topic aliases
- Collection filter, volume filter, open and download buttons
- No OCR or full-text search inside scanned PDFs
- Does not edit or split source PDFs
- Volume number is extracted from directory names such as `Volume_01`
- PDF links use the site's root path, designed for the custom domain `emarkazlibrary.com`

## Files produced

- `emarkaz-books/e-courses/hadith/hadith-search-index.json`
- Existing `index.html` pages at `hadith/` and its individual collection folders
  receive a search button after the normal page generator runs.

## Safety

The one-time hook installer saves your previous generator under
`.git/local-backups/`. A subsequent run of the installer makes no new changes.
You can review the generated changes with `git diff` before committing.
