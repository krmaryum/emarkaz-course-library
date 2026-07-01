#!/usr/bin/env python3
"""
generate_file_pages.py

Auto-generate pages for the eMarkaz Course Library.

Supports:
1. Semester pages:
   books/<course>/semester-01/

2. General nested library pages:
   emarkaz-books/
   quran-juzz/

Run from repo root:
   python generate_file_pages.py
"""

from pathlib import Path
from html import escape
from urllib.parse import quote

BOOKS_DIR = Path("books")
GENERIC_LIBRARY_DIRS = [Path("emarkaz-books"), Path("quran-juzz")]

SUPPORTED_EXTENSIONS = {
    ".pdf":  {"label": "PDF",      "icon": "📕", "open_text": "کتاب کھولیں",  "download_text": "ڈاؤن لوڈ کریں", "can_open": True},
    ".docx": {"label": "DOCX",     "icon": "📘", "open_text": "",             "download_text": "ڈاؤن لوڈ کریں", "can_open": False},
    ".md":   {"label": "Markdown", "icon": "📝", "open_text": "نوٹس کھولیں", "download_text": "ڈاؤن لوڈ کریں", "can_open": True},
    ".xlsx": {"label": "Excel",    "icon": "📊", "open_text": "",             "download_text": "ڈاؤن لوڈ کریں", "can_open": False},
    ".xls":  {"label": "Excel",    "icon": "📊", "open_text": "",             "download_text": "ڈاؤن لوڈ کریں", "can_open": False},
}

COURSE_NAMES = {
    "ac-alim-course": {"ur": "عالم کورس", "en": "AC - Alim Course"},
    "dc-ilm-e-deen-course": {"ur": "علم دین کورس", "en": "DC - Ilm-e-Deen Course"},
    "tif-takhasus-fil-ifta": {"ur": "تخصص فی الافتاء", "en": "TIF - Takhasus fil Ifta"},
    "tfa-takhasus-fil-aqaid": {"ur": "تخصص فی العقائد", "en": "TFA - Takhasus fil Aqaid"},
}

GENERIC_NAMES = {
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
}

def title_from_filename(path: Path) -> str:
    return " ".join(path.stem.replace("_", " ").replace("-", " ").split())

def pretty_folder_name(folder_name: str) -> dict:
    if folder_name in GENERIC_NAMES:
        return GENERIC_NAMES[folder_name]
    clean = " ".join(folder_name.replace("_", " ").replace("-", " ").split())
    return {"ur": clean, "en": clean.title()}

def url_for_file(path: Path) -> str:
    return quote(path.name)

def url_for_folder(path: Path) -> str:
    return quote(path.name) + "/"

def semester_label(folder_name: str) -> str:
    return "سمسٹر " + folder_name.replace("semester-", "")

def home_link(current_folder: Path) -> str:
    depth = len(current_folder.parts)
    return ("../" * depth) + "index.html"

def parent_link(current_folder: Path, root_folder: Path) -> str:
    if current_folder == root_folder:
        return "../index.html"
    return "../"

def page_css():
    return """
    * { margin:0; padding:0; box-sizing:border-box; }
    body { font-family: Arial, "Noto Nastaliq Urdu", "Jameel Noori Nastaleeq", sans-serif; background:linear-gradient(135deg,#f8fafc,#ecfeff); color:#111827; min-height:100vh; line-height:1.9; padding:30px; }
    .container { max-width:1180px; margin:auto; }
    .top-bar { display:flex; justify-content:space-between; align-items:center; gap:16px; margin-bottom:30px; flex-wrap:wrap; }
    .back { display:inline-block; background:#064e3b; color:white; padding:10px 18px; border-radius:12px; text-decoration:none; font-weight:bold; margin-left:8px; }
    .badge { background:#d1fae5; color:#065f46; padding:8px 16px; border-radius:999px; font-weight:bold; border:1px solid #a7f3d0; direction:ltr; }
    .hero { text-align:center; margin-bottom:35px; padding:35px 20px; background:white; border-radius:24px; box-shadow:0 15px 40px rgba(0,0,0,.08); border:1px solid #e5e7eb; }
    .hero h1 { font-size:clamp(32px,5vw,56px); color:#064e3b; margin-bottom:10px; }
    .hero h2 { font-size:24px; color:#374151; margin-bottom:12px; }
    .hero p { color:#4b5563; font-size:18px; }
    .section-title { color:#064e3b; margin:30px 0 18px; font-size:30px; }
    .books-grid,.folders-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:22px; }
    .book-card,.folder-card,.empty-card { background:white; border-radius:22px; padding:24px; border:1px solid #e5e7eb; box-shadow:0 12px 30px rgba(0,0,0,.07); transition:.3s ease; }
    .book-card:hover,.folder-card:hover { transform:translateY(-6px); box-shadow:0 20px 45px rgba(6,95,70,.16); border-color:#10b981; }
    .file-type { display:inline-flex; align-items:center; gap:8px; background:#ecfdf5; color:#065f46; padding:6px 12px; border-radius:999px; font-weight:800; font-size:13px; margin-bottom:14px; direction:ltr; }
    .book-card h3,.folder-card h3 { font-size:22px; color:#111827; margin-bottom:12px; min-height:55px; }
    .english { font-family:Arial,sans-serif; direction:ltr; color:#4b5563; margin-bottom:16px; }
    .buttons { display:flex; gap:10px; flex-wrap:wrap; }
    .btn { display:inline-block; padding:10px 16px; border-radius:12px; text-decoration:none; font-weight:bold; transition:.25s; }
    .open { background:#059669; color:white; }
    .download { background:#1d4ed8; color:white; }
    .btn:hover { opacity:.88; transform:translateY(-2px); }
    footer { text-align:center; margin-top:45px; color:#6b7280; font-size:14px; }
    @media (max-width:600px) { body { padding:18px; } .book-card h3,.folder-card h3 { min-height:auto; } }
    """

def file_cards(files):
    cards = []
    for file_path in files:
        info = SUPPORTED_EXTENSIONS[file_path.suffix.lower()]
        title = escape(title_from_filename(file_path))
        href = escape(url_for_file(file_path))
        buttons = []
        if info["can_open"]:
            buttons.append(f'<a class="btn open" href="{href}" target="_blank" rel="noopener">{escape(info["open_text"])} →</a>')
        buttons.append(f'<a class="btn download" href="{href}" download>{escape(info["download_text"])}</a>')
        cards.append(f"""
      <article class="book-card">
        <div class="file-type"><span>{escape(info["icon"])}</span> {escape(info["label"])}</div>
        <h3>{title}</h3>
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
        <div class="buttons"><a class="btn open" href="{escape(url_for_folder(folder))}">فولڈر کھولیں →</a></div>
      </article>""")
    return "\n".join(cards)

def supported_files_in(folder: Path):
    return sorted([p for p in folder.iterdir() if p.is_file() and p.name not in {"index.html",".gitkeep"} and p.suffix.lower() in SUPPORTED_EXTENSIONS], key=lambda x: x.name.lower())

def subfolders_in(folder: Path):
    return sorted([p for p in folder.iterdir() if p.is_dir() and not p.name.startswith(".")], key=lambda x: x.name.lower())

def is_semester_folder(path: Path) -> bool:
    return path.is_dir() and path.name.startswith("semester-") and path.parent.parent == BOOKS_DIR

def semester_page(course_slug, semester_slug, files):
    course = COURSE_NAMES.get(course_slug, {"ur": course_slug.replace("-", " "), "en": course_slug})
    cards_html = file_cards(files) or """
      <article class="empty-card"><h3>ابھی کوئی فائل شامل نہیں کی گئی</h3><p>اس سمسٹر میں فائل شامل کریں، پھر generator script دوبارہ چلائیں۔</p></article>"""
    return f"""<!DOCTYPE html>
<html lang="ur" dir="rtl"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{escape(course["ur"])} - {escape(semester_label(semester_slug))}</title><style>{page_css()}</style></head>
<body><div class="container">
<div class="top-bar"><div><a class="back" href="../../../index.html">مرکزی صفحہ پر واپس جائیں</a></div><span class="badge">{escape(course["en"])}</span></div>
<section class="hero"><h1>{escape(course["ur"])}</h1><h2>{escape(semester_label(semester_slug))}</h2><p>کل فائلیں: {len(files)}</p></section>
<h2 class="section-title">فائلیں</h2><section class="books-grid">{cards_html}</section>
<footer><p>© eMarkaz Course Library - Auto-generated page</p></footer>
</div></body></html>"""

def generic_page(root_folder: Path, current_folder: Path, subfolders, files):
    names = pretty_folder_name(current_folder.name)
    root_names = pretty_folder_name(root_folder.name)
    folder_html = folder_cards(subfolders) or """
      <article class="empty-card"><h3>کوئی ذیلی فولڈر نہیں</h3><p>یہاں مزید فولڈر شامل کیے جا سکتے ہیں۔</p></article>"""
    file_html = file_cards(files) or """
      <article class="empty-card"><h3>ابھی کوئی فائل شامل نہیں کی گئی</h3><p>اس فولڈر میں فائل شامل کریں، پھر generator script دوبارہ چلائیں۔</p></article>"""
    return f"""<!DOCTYPE html>
<html lang="ur" dir="rtl"><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{escape(names["ur"])} | eMarkaz Course Library</title><style>{page_css()}</style></head>
<body><div class="container">
<div class="top-bar"><div><a class="back" href="{escape(home_link(current_folder))}">مرکزی صفحہ</a><a class="back" href="{escape(parent_link(current_folder, root_folder))}">واپس</a></div><span class="badge">{escape(root_names["en"])}</span></div>
<section class="hero"><h1>{escape(names["ur"])}</h1><h2>{escape(names["en"])}</h2><p>Path: {escape(current_folder.as_posix())}</p><p>ذیلی فولڈرز: {len(subfolders)} | فائلیں: {len(files)}</p></section>
<h2 class="section-title">فولڈرز</h2><section class="folders-grid">{folder_html}</section>
<h2 class="section-title">فائلیں</h2><section class="books-grid">{file_html}</section>
<footer><p>© eMarkaz Course Library - Auto-generated page</p></footer>
</div></body></html>"""

def generate_semester_pages():
    if not BOOKS_DIR.exists():
        print("WARNING: books/ folder not found. Skipping semester pages.")
        return 0
    count = 0
    for semester_folder in sorted([p for p in BOOKS_DIR.glob("*/*") if is_semester_folder(p)]):
        files = supported_files_in(semester_folder)
        html = semester_page(semester_folder.parent.name, semester_folder.name, files)
        (semester_folder / "index.html").write_text(html, encoding="utf-8")
        count += 1
        print(f"Generated semester page: {semester_folder / 'index.html'} ({len(files)} files)")
    return count

def generate_generic_pages():
    count = 0
    for root_folder in GENERIC_LIBRARY_DIRS:
        if not root_folder.exists():
            print(f"WARNING: {root_folder}/ not found. Skipping.")
            continue
        folders = [root_folder] + [p for p in root_folder.rglob("*") if p.is_dir()]
        for folder in sorted(folders, key=lambda x: x.as_posix().lower()):
            html = generic_page(root_folder, folder, subfolders_in(folder), supported_files_in(folder))
            (folder / "index.html").write_text(html, encoding="utf-8")
            count += 1
            print(f"Generated general page: {folder / 'index.html'}")
    return count

def main():
    semester_count = generate_semester_pages()
    generic_count = generate_generic_pages()
    print("\nDone.")
    print(f"Generated {semester_count} semester page(s).")
    print(f"Generated {generic_count} general library page(s).")

if __name__ == "__main__":
    main()
