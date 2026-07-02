# Fix File Order in eMarkaz Library Pages

## Problem

The Quran Juzz page was not showing files in human order.

Example wrong order:

```text
Para 11
Para 10
Para 1
Para 14
Para 13
Para 12
```

This happens because normal text sorting sorts filenames alphabetically.

Alphabetical sorting sees:

```text
1
10
11
12
2
3
```

instead of:

```text
1
2
3
4
...
10
11
12
```

---

## Fix

The updated generator uses natural sorting.

Natural sorting understands numbers inside filenames.

So files now show like this:

```text
Para 1
Para 2
Para 3
...
Para 10
Para 11
Para 12
...
Para 30
```

---

## Updated File

Replace your current generator with:

```text
generate_file_pages.py
```

---

## Install

```bash
cd /c/Linux/emarkaz-course-library

cp /c/Users/krmar/Downloads/generate_file_pages_natural_sort.py generate_file_pages.py
```

---

## Run

```bash
./upload.sh
```

or manually:

```bash
python generate_file_pages.py
git status
git add -A
git commit -m "Fix natural file ordering"
git push origin main
```

---

## What Was Changed

A new function was added:

```python
def natural_key(value):
    text = value.name if isinstance(value, Path) else str(value)
    text = text.lower()
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", text)]
```

Then files and folders are sorted using:

```python
sorted(..., key=natural_key)
```

---

## Result

The Quran Juzz page will show Para files in correct numeric order.
