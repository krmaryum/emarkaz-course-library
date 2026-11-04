#!/usr/bin/env python3
"""Safely add a shared Sahih Bukhari card to AC semesters 10, 11 and 12.
Run from eMarkaz repository root: python add_bukhari_semester_links.py
Makes a timestamped backup and refuses unknown generator structures.
"""
from pathlib import Path
from datetime import datetime
import shutil
import sys

GENERATOR = Path('generate_file_pages.py')
COLLECTION = Path('emarkaz-books/e-courses/hadith/Sahih-Bukhari-Al-Bushra')
MARKER = '# SHARED_BUKHARI_SEMESTER_LINK_V1'

HELPER = '''# SHARED_BUKHARI_SEMESTER_LINK_V1

def shared_bukhari_card(current_folder: Path) -> str:
    """One shared library card on AC semesters 10, 11 and 12 only."""
    import posixpath

    allowed = {
        "books/ac-alim-course/semester-10",
        "books/ac-alim-course/semester-11",
        "books/ac-alim-course/semester-12",
    }
    if current_folder.as_posix() not in allowed:
        return ""

    target = "emarkaz-books/e-courses/hadith/Sahih-Bukhari-Al-Bushra/"
    relative_url = posixpath.relpath(target, start=current_folder.as_posix()) + "/"
    return f\"\"\"
    <h2 class="section-title">مشترکہ کتب خانہ / Shared Library</h2>
    <section class="folders-grid">
      <article class="folder-card searchable-card" data-search="صحیح البخاری البشری sahih bukhari al bushra hadith hades">
        <div class="file-type"><span>📚</span> Shared Collection</div>
        <h3>صحیح البخاری — طبع البشری</h3>
        <p class="english">Sahih Bukhari Al-Bushra · 4 volumes</p>
        <div class="buttons">
          <a class="btn open" href="{escape(relative_url)}">مکمل مجموعہ کھولیں →</a>
        </div>
      </article>
    </section>
\"\"\"

'''

def main():
    if not GENERATOR.is_file():
        sys.exit('ERROR: generate_file_pages.py not found. Run from the repository root.')
    if not COLLECTION.is_dir():
        sys.exit('ERROR: Sahih Bukhari collection folder not found. Please check the destination path.')
    source = GENERATOR.read_text(encoding='utf-8')
    if MARKER in source:
        print('Already installed. No changes made.')
        return
    anchor = 'def library_page(root_folder: Path, current_folder: Path):'
    page_return = '    return f"""<!DOCTYPE html>'
    content_marker = '{search_section}{folders_section}{files_section}'
    if source.count(anchor) != 1 or source.count(page_return) != 1 or source.count(content_marker) != 1:
        sys.exit('ERROR: Generator layout differs from expected version. No changes made. Please share your current generator.')
    patched = source.replace(anchor, HELPER + anchor, 1)
    patched = patched.replace(page_return, '    shared_bukhari_section = shared_bukhari_card(current_folder)\n\n' + page_return, 1)
    patched = patched.replace(content_marker, content_marker + '{shared_bukhari_section}', 1)
    try:
        compile(patched, str(GENERATOR), 'exec')
    except SyntaxError as exc:
        sys.exit(f'ERROR: Validation failed ({exc}). Original unchanged.')
    backup_dir = Path('.git/local-backups') if Path('.git').is_dir() else Path('../eMarkaz-local-backups')
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / ('generate_file_pages.backup-' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.py')
    shutil.copy2(GENERATOR, backup)
    GENERATOR.write_text(patched, encoding='utf-8')
    print('SUCCESS: Shared Sahih Bukhari links installed for AC Semesters 10, 11, 12.')
    print(f'Backup saved: {backup}')
    print('Next: python generate_file_pages.py')

if __name__ == '__main__':
    main()
