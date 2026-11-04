#!/usr/bin/env python3
"""Safely add Sahih Muslim alongside Bukhari on AC semesters 10, 11 and 12.
Run from the eMarkaz repository root: python add_sahih_muslim_shared_links.py
Only replaces the shared_bukhari_card() implementation, preserving search hooks.
"""
from pathlib import Path
import ast
import re
import sys

GENERATOR = Path('generate_file_pages.py')
START = 'def shared_bukhari_card(current_folder: Path) -> str:'
END = 'def library_page('

REPLACEMENT = '''def shared_bukhari_card(current_folder: Path) -> str:
    """Shared Hadith library cards for AC semesters 10, 11 and 12."""
    import posixpath

    allowed = {
        "books/ac-alim-course/semester-10",
        "books/ac-alim-course/semester-11",
        "books/ac-alim-course/semester-12",
    }
    if current_folder.as_posix() not in allowed:
        return ""

    collections = [
        (
            "emarkaz-books/e-courses/hadith/Sahih-Bukhari-Al-Bushra/",
            "صحیح البخاری — طبع البشری",
            "Sahih Bukhari Al-Bushra · 4 volumes",
            "صحیح البخاری البشری sahih bukhari al bushra hadith",
        ),
        (
            "emarkaz-books/e-courses/hadith/Sahih_Muslim/",
            "صحیح مسلم — مکمل مجموعہ",
            "Sahih Muslim · 7 volumes",
            "صحیح مسلم sahih muslim muslim bushra hadith",
        ),
    ]
    cards = []
    for target, urdu_title, english_title, search_words in collections:
        relative_url = posixpath.relpath(target.rstrip("/"), start=current_folder.as_posix()) + "/"
        cards.append(f\"\"\"
      <article class="folder-card searchable-card" data-search="{escape(search_words, quote=True)}">
        <div class="file-type"><span>📚</span> Shared Collection</div>
        <h3>{escape(urdu_title)}</h3>
        <p class="english">{escape(english_title)}</p>
        <div class="buttons">
          <a class="btn open" href="{escape(relative_url, quote=True)}">مکمل مجموعہ کھولیں →</a>
        </div>
      </article>\"\"\")
    return (
        '<h2 class="section-title">مشترکہ کتب خانہ / Shared Library</h2>\\n'
        '<section class="folders-grid">\\n'
        + "\\n".join(cards)
        + "\\n</section>"
    )

'''

def main():
    if not GENERATOR.is_file():
        sys.exit('ERROR: Run this script from the repository root next to generate_file_pages.py.')
    original = GENERATOR.read_text(encoding='utf-8')
    start = original.find(START)
    if start == -1:
        sys.exit('ERROR: Shared Bukhari function not found. No changes made.')
    end = original.find(END, start)
    if end == -1:
        sys.exit('ERROR: library_page() boundary not found. No changes made.')
    section = original[start:end]
    if section.count('def shared_bukhari_card(') != 1:
        sys.exit('ERROR: Unexpected source structure. No changes made.')
    if 'Sahih_Muslim/' in section and 'Sahih-Bukhari-Al-Bushra/' in section:
        print('Already updated: Bukhari and Muslim cards found. No changes required.')
        return
    updated = original[:start] + REPLACEMENT + original[end:]
    ast.parse(updated, filename=str(GENERATOR))
    backup_dir = Path('.git/local-backups')
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / 'generate_file_pages_before_muslim_shared_links.py'
    if backup.exists():
        sys.exit(f'ERROR: Backup already exists: {backup}. Please preserve it and inspect before retrying.')
    backup.write_text(original, encoding='utf-8')
    GENERATOR.write_text(updated, encoding='utf-8')
    print('Updated generate_file_pages.py (Bukhari + Muslim on AC semesters 10–12).')
    print(f'Backup: {backup}')
    print('Next: python generate_file_pages.py')

if __name__ == '__main__':
    main()
