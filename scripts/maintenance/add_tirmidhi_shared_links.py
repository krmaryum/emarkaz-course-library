#!/usr/bin/env python3
"""Add Jami al-Tirmidhi to AC semester 10/11/12 shared cards.

Run from eMarkaz repository root. Preserves existing Bukhari/Muslim cards,
all other generator code, Hadith search hooks, and dark styling.
"""
from pathlib import Path
import ast
import sys

GENERATOR = Path('generate_file_pages.py')
TIRMIDHI_PATH = 'emarkaz-books/e-courses/hadith/JAMI_AL_TIRMIZI_BUSHRA/'
BACKUP = Path('.git/local-backups/generate_file_pages_before_tirmidhi_shared_links.py')

TIRMIDHI_ENTRY = '''        (
            "emarkaz-books/e-courses/hadith/JAMI_AL_TIRMIZI_BUSHRA/",
            "جامع الترمذی — طبع البشری",
            "Jami al-Tirmidhi Al-Bushra · 5 volumes",
            "جامع الترمذی ترمذی سنن الترمذی tirmidhi tirimizi jami al tirmidhi hadith",
        ),'''


def main():
    if not GENERATOR.is_file() or not Path('.git').is_dir():
        sys.exit('ERROR: Run from the root of your emarkaz-course-library Git repository.')
    if not Path(TIRMIDHI_PATH).is_dir():
        sys.exit(f'ERROR: Tirmidhi collection folder missing: {TIRMIDHI_PATH}')
    original = GENERATOR.read_text(encoding='utf-8')
    tree = ast.parse(original, filename=str(GENERATOR))
    shared = next((n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                   and n.name == 'shared_bukhari_card'), None)
    if not shared:
        sys.exit('ERROR: Shared-library function missing. No changes made.')
    collection_assignments = [n for n in ast.walk(shared)
                              if isinstance(n, ast.Assign)
                              and isinstance(n.value, ast.List)
                              and any(isinstance(t, ast.Name) and t.id == 'collections' for t in n.targets)]
    if len(collection_assignments) != 1:
        sys.exit('ERROR: Expected one collections = [...] list inside shared_bukhari_card. No changes made.')
    collection_list = collection_assignments[0].value
    paths = []
    for entry in collection_list.elts:
        if isinstance(entry, ast.Tuple) and entry.elts:
            first = entry.elts[0]
            if isinstance(first, ast.Constant) and isinstance(first.value, str):
                paths.append(first.value)
    if TIRMIDHI_PATH in paths:
        print('Tirmidhi already exists in shared collections. No changes required.')
        return
    if not any('Sahih-Bukhari-Al-Bushra/' in p for p in paths) or not any('Sahih_Muslim/' in p for p in paths):
        sys.exit('ERROR: Expected existing Bukhari and Muslim cards. No changes made.')
    lines = original.splitlines(keepends=True)
    closing_line_index = collection_list.end_lineno - 1
    if lines[closing_line_index].strip() != ']':
        sys.exit('ERROR: Unexpected collection list formatting. No changes made.')
    lines.insert(closing_line_index, TIRMIDHI_ENTRY + '\n')
    updated = ''.join(lines)
    ast.parse(updated, filename=str(GENERATOR))
    if BACKUP.exists():
        sys.exit(f'ERROR: Backup already exists at {BACKUP}; please inspect before rerunning.')
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    BACKUP.write_text(original, encoding='utf-8')
    GENERATOR.write_text(updated, encoding='utf-8')
    print('SUCCESS: Added Jami al-Tirmidhi (5 volumes) alongside Bukhari and Muslim.')
    print('Shared links will appear on AC Semester 10, 11, and 12 after regeneration.')
    print('Generator backup:', BACKUP)
    print('NEXT: python generate_file_pages.py')

if __name__ == '__main__':
    main()
