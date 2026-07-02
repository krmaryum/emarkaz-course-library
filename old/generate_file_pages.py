#!/usr/bin/env python3
"""
generate_file_pages.py

Auto-generate pages for the eMarkaz Course Library.

Controlled flexible version:
- Generates pages for approved public library roots only.
- Keeps special course/semester handling for books/.
- Supports nested folders.
- Keeps generated pages clean and professional.

Default public roots:
    books/
    emarkaz-books/
    quran-juzz/

To add a new public root later:
    Add the folder name to PUBLIC_LIBRARY_ROOTS.

Example:
    PUBLIC_LIBRARY_ROOTS = [
        "books",
        "emarkaz-books",
        "quran-juzz",
        "arabic-books",
    ]

Run from repo root:
    python generate_file_pages.py
"""

from pathlib import Path
from html import escape
from urllib.parse import quote
import re

# ============================================================
# Controlled public roots
# ============================================================
# The generator will ONLY create pages inside these root folders.
# This avoids accidentally generating pages inside .git, assets, old, etc.
PUBLIC_LIBRARY_ROOTS = [
    "books",
    "emarkaz-books",
    "quran-juzz",
]

BOOKS_DIR = Path("books")

SUPPORTED_EXTENSIONS = {
    ".pdf":  {"label": "PDF",      "icon": "📕", "open_text": "کتاب کھولیں",  "download_text": "ڈاؤن لوڈ کریں", "can_open": True},
    ".docx": {"label": "DOCX",     "icon": "📘", "open_text": "",             "download_text": "ڈاؤن لوڈ کریں", "can_open": False},
    ".md":   {"label": "Markdown", "icon": "📝", "open_text": "نوٹس کھولیں", "download_text": "ڈاؤن لوڈ کریں", "can_open": True},
    ".xlsx": {"label": "Excel",    "icon": "📊", "open_text": "",             "download_text": "ڈاؤن لوڈ کریں", "can_open": False},
    ".xls":  {"label": "Excel",    "icon": "📊", "open_text": "",             "download_text": "ڈاؤن لوڈ کریں", "can_open": False},
    ".txt":  {"label": "Text",     "icon": "📄", "open_text": "فائل کھولیں", "download_text": "ڈاؤن لوڈ کریں", "can_open": True},
}

COURSE_NAMES = {
    "ac-alim-course": {"ur": "عالم کورس", "en": "AC - Alim Course"},
    "dc-ilm-e-deen-course": {"ur": "علم دین کورس", "en": "DC - Ilm-e-Deen Course"},
    "tif-takhasus-fil-ifta": {"ur": "تخصص فی الافتاء", "en": "TIF - Takhasus fil Ifta"},
    "tfa-takhasus-fil-aqaid": {"ur": "تخصص فی العقائد", "en": "TFA - Takhasus fil Aqaid"},
}

NAME_MAP = {
    "books": {"ur": "کورس کتابیں", "en": "Course Books"},
    "emarkaz-books": {"ur": "ای مرکز کتابیں", "en": "eMarkaz Books"},
    "quran-juzz": {"ur": "قرآن پارے", "en": "Quran Juzz"},
    "e-courses": {"ur": "ای کورسز", "en": "E-Courses"},
    "advanced-topics": {"ur": "Advanced Topics", "en": "Advanced Topics"},
    "aqaid": {"ur": "عقائد", "en": "Aqaid"},
    "baray-ustaz-jee": {"ur": "بڑے استاذ جی", "en": "Baray Ustaz Jee"},
    "fataws": {"ur": "فتاویٰ", "en": "Fatawa"},
    "fiqh": {"ur": "فقہ", "en": "Fiqh"},
    "grammar": {"ur": "گرامر", "en": "Grammar"},
    "nawh": {"ur": "نحو", "en": "Nahw"},
    "surf": {"ur": "صرف", "en": "Sarf"},
    "hadith": {"ur": "حدیث", "en": "Hadith"},
    "meeraas": {"ur": "میراث", "en": "Meeraas"},
    "personalities": {"ur": "شخصیات", "en": "Personalities"},
    "Prophets": {"ur": "انبیاء", "en": "Prophets"},
    "Sahabas": {"ur": "صحابہ", "en": "Sahabas"},
    "Scholars": {"ur": "علماء", "en": "Scholars"},
    "Walees": {"ur": "اولیاء", "en": "Walees"},
    "Exam Papers": {"ur": "امتحانی پرچے", "en": "Exam Papers"},
}

SKIP_DIR_NAMES = {
    ".git",
    ".github",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
}

SKIP_FILE_NAMES = {
    "index.html",
    ".gitkeep",
    ".DS_Store",
}

def clean_name(text: str) -> str:
    return " ".join(text.replace("_", " ").replace("-", " ").split())

def title_from_filename(path: Path) -> str:
    return clean_name(path.stem)

def pretty_folder_name(folder_name: str) -> dict:
    if folder_name in NAME_MAP:
        return NAME_MAP[folder_name]
    clean = clean_name(folder_name)
    return {"ur": clean, "en": clean.title()}

def semester_label(folder_name: str) -> str:
    match = re.search(r"semester-(\d+)", folder_name, re.IGNORECASE)
    if match:
        return "سمسٹر " + f"{int(match.group(1)):02d}"
    return clean_name(folder_name)

def semester_en_label(folder_name: str) -> str:
    match = re.search(r"semester-(\d+)", folder_name, re.IGNORECASE)
    if match:
        return "Semester " + f"{int(match.group(1)):02d}"
    return clean_name(folder_name).title()

def url_for_file(path: Path) -> str:
    return quote(path.name)

def url_for_folder(path: Path) -> str:
    return quote(path.name) + "/"

def root_home_link(current_folder: Path) -> str:
    return ("../" * len(current_folder.parts)) + "index.html"

def parent_link(current_folder: Path, root_folder: Path) -> str:
    if current_folder == root_folder:
        return root_home_link(current_folder)
    return "../"

def page_css() -> str:
    return """
    * { margin:0; padding:0; box-sizing:border-box; }
    body {
      font-family: Arial, "Noto Nastaliq Urdu", "Jameel Noori Nastaleeq", sans-serif;
      background:linear-gradient(135deg,#f8fafc,#ecfeff);
      color:#111827;
      min-height:100vh;
      line-height:1.9;
      padding:30px;
    }
    .container { max-width:1180px; margin:auto; }
    .top-bar {
      display:flex;
      justify-content:space-between;
      align-items:center;
      gap:16px;
      margin-bottom:30px;
      flex-wrap:wrap;
    }
    .back {
      display:inline-block;
      background:#064e3b;
      color:white;
      padding:10px 18px;
      border-radius:12px;
      text-decoration:none;
      font-weight:bold;
      margin-left:8px;
    }
    .badge {
      background:#d1fae5;
      color:#065f46;
      padding:8px 16px;
      border-radius:999px;
      font-weight:bold;
      border:1px solid #a7f3d0;
      direction:ltr;
    }
    .hero {
      text-align:center;
      margin-bottom:35px;
      padding:35px 20px;
      background:white;
      border-radius:24px;
      box-shadow:0 15px 40px rgba(0,0,0,.08);
      border:1px solid #e5e7eb;
    }
    .hero h1 {
      font-size:clamp(32px,5vw,56px);
      color:#064e3b;
      margin-bottom:10px;
    }
    .hero h2 {
      font-size:24px;
      color:#374151;
      margin-bottom:0;
      direction:ltr;
    }
    .section-title {
      color:#064e3b;
      margin:30px 0 18px;
      font-size:30px;
    }
    .books-grid,.folders-grid {
      display:grid;
      grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
      gap:22px;
    }
    .book-card,.folder-card,.empty-card {
      background:white;
      border-radius:22px;
      padding:24px;
      border:1px solid #e5e7eb;
      box-shadow:0 12px 30px rgba(0,0,0,.07);
      transition:.3s ease;
    }
    .book-card:hover,.folder-card:hover {
      transform:translateY(-6px);
      box-shadow:0 20px 45px rgba(6,95,70,.16);
      border-color:#10b981;
    }
    .file-type {
      display:inline-flex;
      align-items:center;
      gap:8px;
      background:#ecfdf5;
      color:#065f46;
      padding:6px 12px;
      border-radius:999px;
      font-weight:800;
      font-size:13px;
      margin-bottom:14px;
      direction:ltr;
    }
    .book-card h3,.folder-card h3 {
      font-size:22px;
      color:#111827;
      margin-bottom:12px;
      min-height:55px;
    }
    .english {
      font-family:Arial,sans-serif;
      direction:ltr;
      color:#4b5563;
      margin-bottom:16px;
    }
    .buttons { display:flex; gap:10px; flex-wrap:wrap; }
    .btn {
      display:inline-block;
      padding:10px 16px;
      border-radius:12px;
      text-decoration:none;
      font-weight:bold;
      transition:.25s;
    }
    .open { background:#059669; color:white; }
    .download { background:#1d4ed8; color:white; }
    .btn:hover { opacity:.88; transform:translateY(-2px); }
    footer {
      text-align:center;
      margin-top:45px;
      color:#6b7280;
      font-size:14px;
    }
    @media (max-width:600px) {
      body { padding:18px; }
      .book-card h3,.folder-card h3 { min-height:auto; }
    }
    """

def is_skipped_dir(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)

def supported_files_in(folder: Path):
    return sorted([
        p for p in folder.iterdir()
        if p.is_file()
        and p.name not in SKIP_FILE_NAMES
        and p.suffix.lower() in SUPPORTED_EXTENSIONS
    ], key=lambda x: x.name.lower())

def subfolders_in(folder: Path):
    return sorted([
        p for p in folder.iterdir()
        if p.is_dir()
        and not p.name.startswith(".")
        and p.name not in SKIP_DIR_NAMES
    ], key=lambda x: x.name.lower())

def file_cards(files):
    cards = []
    for file_path in files:
        info = SUPPORTED_EXTENSIONS[file_path.suffix.lower()]
        buttons = []
        if info["can_open"]:
            buttons.append(
                f'<a class="btn open" href="{escape(url_for_file(file_path))}" target="_blank" rel="noopener">{escape(info["open_text"])} →</a>'
            )
        buttons.append(
            f'<a class="btn download" href="{escape(url_for_file(file_path))}" download>{escape(info["download_text"])}</a>'
        )

        cards.append(f"""
      <article class="book-card">
        <div class="file-type"><span>{escape(info["icon"])}</span> {escape(info["label"])}</div>
        <h3>{escape(title_from_filename(file_path))}</h3>
        <div class="buttons">{' '.join(buttons)}</div>
      </article>""")
    return "\n".join(cards)

def folder_cards(folders):
    cards = []
    for folder in folders:
        names = pretty_folder_name(folder.name)
        cards.append(f"""
      <article class="folder-card">
        <div class="file-type"><span>📁</span> Folder</div>
        <h3>{escape(names["ur"])}</h3>
        <p class="english">{escape(names["en"])}</p>
        <div class="buttons">
          <a class="btn open" href="{escape(url_for_folder(folder))}">فولڈر کھولیں →</a>
        </div>
      </article>""")
    return "\n".join(cards)

def find_semester_root(folder: Path):
    parts = folder.parts
    for part_index, part in enumerate(parts):
        if part.lower().startswith("semester-"):
            return Path(*parts[:part_index + 1])
    return None

def display_names_for_page(root_folder: Path, current_folder: Path):
    # Special handling for course semester folders inside books/<course>/semester-XX
    if root_folder == BOOKS_DIR:
        semester_root = find_semester_root(current_folder)

        if semester_root and len(semester_root.parts) >= 3:
            course_slug = semester_root.parent.name
            semester_slug = semester_root.name
            course = COURSE_NAMES.get(course_slug, {"ur": clean_name(course_slug), "en": clean_name(course_slug).title()})

            if current_folder == semester_root:
                title_ur = f'{course["ur"]} - {semester_label(semester_slug)}'
                title_en = f'{course["en"]} - {semester_en_label(semester_slug)}'
            else:
                folder_names = pretty_folder_name(current_folder.name)
                title_ur = folder_names["ur"]
                title_en = f'{course["en"]} / {semester_en_label(semester_slug)} / {folder_names["en"]}'

            badge = course["en"]
            return title_ur, title_en, badge

    names = pretty_folder_name(current_folder.name)
    root_names = pretty_folder_name(root_folder.name)
    return names["ur"], names["en"], root_names["en"]

def library_page(root_folder: Path, current_folder: Path):
    subfolders = subfolders_in(current_folder)
    files = supported_files_in(current_folder)
    title_ur, title_en, badge = display_names_for_page(root_folder, current_folder)

    folders_section = ""
    if subfolders:
        folders_section = f"""
    <h2 class="section-title">فولڈرز</h2>
    <section class="folders-grid">
{folder_cards(subfolders)}
    </section>
"""

    files_section = ""
    if files:
        files_section = f"""
    <h2 class="section-title">فائلیں</h2>
    <section class="books-grid">
{file_cards(files)}
    </section>
"""
    elif not subfolders:
        files_section = """
    <h2 class="section-title">فائلیں</h2>
    <section class="books-grid">
      <article class="empty-card">
        <h3>ابھی کوئی فائل شامل نہیں کی گئی</h3>
        <p>اس فولڈر میں فائل شامل کریں، پھر generator script دوبارہ چلائیں۔</p>
      </article>
    </section>
"""

    return f"""<!DOCTYPE html>
<html lang="ur" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape(title_ur)} | eMarkaz Course Library</title>
  <style>{page_css()}</style>
</head>
<body>
  <div class="container">
    <div class="top-bar">
      <div>
        <a class="back" href="{escape(root_home_link(current_folder))}">مرکزی صفحہ</a>
        <a class="back" href="{escape(parent_link(current_folder, root_folder))}">واپس</a>
      </div>
      <span class="badge">{escape(badge)}</span>
    </div>

    <section class="hero">
      <h1>{escape(title_ur)}</h1>
      <h2>{escape(title_en)}</h2>
    </section>
{folders_section}{files_section}
    <footer>
      <p>© eMarkaz Course Library - Auto-generated page</p>
    </footer>
  </div>
</body>
</html>
"""

def generate_pages_for_root(root_folder: Path) -> int:
    if not root_folder.exists():
        print(f"WARNING: {root_folder}/ not found. Skipping.")
        return 0

    if not root_folder.is_dir():
        print(f"WARNING: {root_folder} is not a folder. Skipping.")
        return 0

    folders = [root_folder] + [
        p for p in root_folder.rglob("*")
        if p.is_dir() and not is_skipped_dir(p)
    ]

    count = 0
    for folder in sorted(folders, key=lambda x: x.as_posix().lower()):
        html = library_page(root_folder, folder)
        output_file = folder / "index.html"
        output_file.write_text(html, encoding="utf-8")
        count += 1
        print(f"Generated page: {output_file}")

    return count

def main():
    total_count = 0

    print("Approved public library roots:")
    for root in PUBLIC_LIBRARY_ROOTS:
        print(f"- {root}")

    print()

    for root in PUBLIC_LIBRARY_ROOTS:
        total_count += generate_pages_for_root(Path(root))

    print("\nDone.")
    print(f"Generated {total_count} page(s).")

if __name__ == "__main__":
    main()
