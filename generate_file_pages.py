#!/usr/bin/env python3
"""
generate_file_pages.py

Auto-generate semester index.html pages for the eMarkaz Course Library.

Supported files:
- .pdf   -> Open + Download
- .docx  -> Download
- .md    -> Open + Download
- .xlsx  -> Download

How to use:
1. Put this file in the root of your repository:
   /c/Linux/emarkaz-course-library/generate_file_pages.py

2. Add your course files inside semester folders, for example:
   books/ac-alim-course/semester-01/book.pdf

3. Run:
   python generate_file_pages.py

4. Commit and push:
   git add -A
   git commit -m "Auto-generate course file pages"
   git push origin main
"""

from pathlib import Path
from html import escape
from urllib.parse import quote

BOOKS_DIR = Path("books")
SUPPORTED_EXTENSIONS = {
    ".pdf": {
        "label": "PDF",
        "icon": "📕",
        "open_text": "کتاب کھولیں",
        "download_text": "ڈاؤن لوڈ کریں",
        "can_open": True,
    },
    ".docx": {
        "label": "DOCX",
        "icon": "📘",
        "open_text": "",
        "download_text": "ڈاؤن لوڈ کریں",
        "can_open": False,
    },
    ".md": {
        "label": "Markdown",
        "icon": "📝",
        "open_text": "نوٹس کھولیں",
        "download_text": "ڈاؤن لوڈ کریں",
        "can_open": True,
    },
    ".xlsx": {
        "label": "Excel",
        "icon": "📊",
        "open_text": "",
        "download_text": "ڈاؤن لوڈ کریں",
        "can_open": False,
    },
}

COURSE_NAMES = {
    "ac-alim-course": {"ur": "عالم کورس", "en": "AC - Alim Course"},
    "dc-ilm-e-deen-course": {"ur": "علم دین کورس", "en": "DC - Ilm-e-Deen Course"},
    "tif-takhasus-fil-ifta": {"ur": "تخصص فی الافتاء", "en": "TIF - Takhasus fil Ifta"},
    "tfa-takhasus-fil-aqaid": {"ur": "تخصص فی العقائد", "en": "TFA - Takhasus fil Aqaid"},
}


def title_from_filename(path: Path) -> str:
    """Return a clean title from filename without extension."""
    title = path.stem.replace("_", " ").replace("-", " ")
    # Keep Urdu/Arabic as-is, but clean repeated spaces.
    return " ".join(title.split())


def url_for_file(path: Path) -> str:
    """URL-encode filename safely while keeping relative path simple."""
    return quote(path.name)


def semester_label(folder_name: str) -> str:
    """Convert semester-01 to سمسٹر 01."""
    number = folder_name.replace("semester-", "")
    return f"سمسٹر {number}"


def generate_cards(files):
    cards = []
    for file_path in files:
        ext = file_path.suffix.lower()
        info = SUPPORTED_EXTENSIONS[ext]
        title = escape(title_from_filename(file_path))
        href = escape(url_for_file(file_path))
        label = escape(info["label"])
        icon = escape(info["icon"])

        buttons = []
        if info["can_open"]:
            buttons.append(
                f'<a class="btn open" href="{href}" target="_blank" rel="noopener">{escape(info["open_text"])} →</a>'
            )
        buttons.append(
            f'<a class="btn download" href="{href}" download>{escape(info["download_text"])}</a>'
        )

        cards.append(f"""
      <article class="book-card">
        <div class="file-type"><span>{icon}</span> {label}</div>
        <h3>{title}</h3>
        <div class="buttons">
          {' '.join(buttons)}
        </div>
      </article>""")
    return "\n".join(cards)


def page_template(course_slug: str, semester_slug: str, files):
    course = COURSE_NAMES.get(course_slug, {"ur": course_slug.replace("-", " "), "en": course_slug})
    course_ur = escape(course["ur"])
    course_en = escape(course["en"])
    sem_ur = escape(semester_label(semester_slug))
    cards_html = generate_cards(files)
    total_files = len(files)

    if not cards_html.strip():
        cards_html = """
      <article class="empty-card">
        <h3>ابھی کوئی فائل شامل نہیں کی گئی</h3>
        <p>اس سمسٹر میں PDF، DOCX، MD، یا XLSX فائل شامل کریں، پھر generator script دوبارہ چلائیں۔</p>
      </article>"""

    return f"""<!DOCTYPE html>
<html lang="ur" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{course_ur} - {sem_ur}</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: Arial, "Noto Nastaliq Urdu", "Jameel Noori Nastaleeq", sans-serif;
      background: linear-gradient(135deg, #f8fafc, #ecfeff);
      color: #111827;
      min-height: 100vh;
      line-height: 1.9;
      padding: 30px;
    }}
    .container {{ max-width: 1180px; margin: auto; }}
    .top-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      margin-bottom: 30px;
      flex-wrap: wrap;
    }}
    .back {{
      display: inline-block;
      background: #064e3b;
      color: white;
      padding: 10px 18px;
      border-radius: 12px;
      text-decoration: none;
      font-weight: bold;
    }}
    .badge {{
      background: #d1fae5;
      color: #065f46;
      padding: 8px 16px;
      border-radius: 999px;
      font-weight: bold;
      border: 1px solid #a7f3d0;
      direction: ltr;
    }}
    .hero {{
      text-align: center;
      margin-bottom: 35px;
      padding: 35px 20px;
      background: white;
      border-radius: 24px;
      box-shadow: 0 15px 40px rgba(0,0,0,0.08);
      border: 1px solid #e5e7eb;
    }}
    .hero h1 {{ font-size: clamp(32px, 5vw, 56px); color: #064e3b; margin-bottom: 10px; }}
    .hero h2 {{ font-size: 24px; color: #374151; margin-bottom: 12px; }}
    .hero p {{ color: #4b5563; font-size: 18px; }}
    .books-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 22px;
    }}
    .book-card, .empty-card {{
      background: white;
      border-radius: 22px;
      padding: 24px;
      border: 1px solid #e5e7eb;
      box-shadow: 0 12px 30px rgba(0,0,0,0.07);
      transition: 0.3s ease;
    }}
    .book-card:hover {{
      transform: translateY(-6px);
      box-shadow: 0 20px 45px rgba(6,95,70,0.16);
      border-color: #10b981;
    }}
    .file-type {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #ecfdf5;
      color: #065f46;
      padding: 6px 12px;
      border-radius: 999px;
      font-weight: 800;
      font-size: 13px;
      margin-bottom: 14px;
      direction: ltr;
    }}
    .book-card h3 {{ font-size: 22px; color: #111827; margin-bottom: 18px; min-height: 65px; }}
    .buttons {{ display: flex; gap: 10px; flex-wrap: wrap; }}
    .btn {{
      display: inline-block;
      padding: 10px 16px;
      border-radius: 12px;
      text-decoration: none;
      font-weight: bold;
      transition: 0.25s;
    }}
    .open {{ background: #059669; color: white; }}
    .download {{ background: #1d4ed8; color: white; }}
    .btn:hover {{ opacity: 0.88; transform: translateY(-2px); }}
    footer {{ text-align: center; margin-top: 45px; color: #6b7280; font-size: 14px; }}
    @media (max-width: 600px) {{
      body {{ padding: 18px; }}
      .book-card h3 {{ min-height: auto; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="top-bar">
      <a class="back" href="../../../index.html">مرکزی صفحہ پر واپس جائیں</a>
      <span class="badge">{course_en}</span>
    </div>

    <section class="hero">
      <h1>{course_ur}</h1>
      <h2>{sem_ur}</h2>
      <p>اس صفحہ پر اس سمسٹر کی تمام دستیاب فائلیں موجود ہیں۔ کل فائلیں: {total_files}</p>
    </section>

    <section class="books-grid">
{cards_html}
    </section>

    <footer>
      <p>© eMarkaz Course Library - Auto-generated page</p>
    </footer>
  </div>
</body>
</html>
"""


def is_semester_folder(path: Path) -> bool:
    return path.is_dir() and path.name.startswith("semester-") and path.parent.parent == BOOKS_DIR


def main():
    if not BOOKS_DIR.exists():
        raise SystemExit("ERROR: books/ folder not found. Run this script from the repo root.")

    generated_count = 0
    semester_folders = sorted([p for p in BOOKS_DIR.glob("*/*") if is_semester_folder(p)])

    for semester_folder in semester_folders:
        files = sorted(
            [p for p in semester_folder.iterdir()
             if p.is_file()
             and p.name != "index.html"
             and p.name != ".gitkeep"
             and p.suffix.lower() in SUPPORTED_EXTENSIONS],
            key=lambda x: x.name.lower()
        )

        course_slug = semester_folder.parent.name
        semester_slug = semester_folder.name
        html = page_template(course_slug, semester_slug, files)
        output_file = semester_folder / "index.html"
        output_file.write_text(html, encoding="utf-8")
        generated_count += 1
        print(f"Generated: {output_file} ({len(files)} files)")

    print(f"\nDone. Generated {generated_count} semester page(s).")


if __name__ == "__main__":
    main()
